from django.conf import settings
from django.utils import simplejson as json
from django.contrib.auth.models import User

from .. import models
from .. import views

import test_utils
import mock
from nose.tools import eq_, ok_
from webpagemaker.browserid_ajax.tests import fake_verify_success

SIMPLE_HTML = "<!DOCTYPE html><html><head><title>hi</title></head>" + \
              "<body>hello.</body></html>"

class FakeCache(object):
    keys = {}
    
    @classmethod
    def set(cls, key, value, timeout):
        cls.keys[key] = {'value': value, 'timeout': timeout}
    
    @classmethod
    def get(cls, key):
        return cls.keys.get(key, {'value': None})['value']

def page_from_publish(response):
    """
    Given a successful POST request to /api/page, return the
    corresponding Page object that was created.
    """
    
    short_url_id = response.content.split('/')[-2]
    return models.Page.objects.get(short_url_id=short_url_id)

class PublishAuthTests(test_utils.TestCase):
    def tearDown(self):
        self.client.logout()
        User.objects.all().delete()
    
    def test_anonymous_publish_has_no_creator(self):
        response = self.client.post('/api/page', {'html': 'hi'})
        eq_(page_from_publish(response).creator, None)

    @mock.patch('django_browserid.auth.verify', fake_verify_success)
    def test_authenticated_publish_has_creator(self):
        user = User(username='foo', password='meh', email='foo@foo.org')
        user.save()
        self.client.login(assertion='foo@foo.org', audience='lol')
        response = self.client.post('/api/page', {'html': 'hi'})
        page = page_from_publish(response)
        eq_(page.creator, user)
        eq_(user.pages.count(), 1)
        eq_(user.pages.all()[0], page)
    
class PublishTests(test_utils.TestCase):
    def _publish_and_verify(self, html, expected_html=None):
        """
        Publish the given string of valid HTML5, then fetch it back and
        make sure it's identical to our expectation. If no expectation
        is provided, it's assumed we expect the exact same input handed
        back to us.
        """

        if expected_html is None:
            expected_html = html
        response = self.client.post('/api/page', {'html': html})
        eq_(response.status_code, 200)
        eq_(response['Access-Control-Allow-Origin'], '*')

        page_id = response.content
        response = self.client.get(page_id)
        eq_(response.status_code, 200)
        eq_(response['Access-Control-Allow-Origin'], '*')
        eq_(response['Content-Type'], 'text/html; charset=utf-8')
        eq_(type(response.content), str)
        eq_(response.content, expected_html)
        return response

    def test_get_with_and_without_slash(self):
        response = self.client.post('/api/page', {
          'html': 'hi',
          'original-url': 'http://foo.com/'
          })
        url = response.content;
        response = self.client.get(url, follow=True)
        slashed = response.content
        url_noslash = url[0:-1]
        response = self.client.get(url_noslash, follow=True)
        unslashed = response.content
        eq_(slashed, unslashed)

    def test_get_sanitizer_config(self):
        response = self.client.get('/api/config')
        eq_(response.status_code, 200)
        cfg = json.loads(response.content)
        ok_('a' in cfg['allowed_tags'])
        ok_('href' in cfg['allowed_attributes']['a'])
        eq_(response['Access-Control-Allow-Origin'], '*')

    def test_massive_content_is_rejected(self):
        massive_content = "*" * (settings.MAX_PUBLISHED_PAGE_SIZE + 1)
        response = self.client.post('/api/page', {'html': massive_content})
        eq_(response.status_code, 413)
        eq_(response.content, "Request Entity Too Large")

    def test_long_origin_url_is_truncated(self):
        response = self.client.post('/api/page', {
          'html': 'hi',
          'original-url': 'http://foo.com/%s' % ('*' * 5000)
          })
        eq_(response.status_code, 200)

    def test_bad_origin_url_is_rejected(self):
        response = self.client.post('/api/page', {
          'html': 'hi',
          'original-url': 'javascript:LOL'
          })
        eq_(response.status_code, 400)
        eq_(response.content, "Invalid origin URL.")

    def test_good_origin_url_is_accepted(self):
        response = self.client.post('/api/page', {
          'html': 'hi',
          'original-url': 'http://foo.com/'
          })
        eq_(response.status_code, 200)

    def test_blank_origin_url_is_accepted(self):
        response = self.client.post('/api/page', {
          'html': 'hi',
          'original-url': ''
          })
        eq_(response.status_code, 200)
    
    def test_page_source_is_plaintext(self):
        response = self.client.post('/api/page', {
          'html': '<script>alert("YO");</script>'
          })
        src_response = self.client.get(response.content + 'raw')
        eq_(src_response['Content-Type'], 'text/plain')
        eq_(src_response.content, '<script>alert("YO");</script>')

    def test_origin_url_is_returned(self):
        response = self.client.post('/api/page', {
          'html': 'hi',
          'original-url': 'http://blah.com/'
          })
        response = self.client.get(response.content)
        eq_(response['x-original-url'], 'http://blah.com/')

    def test_published_pages_are_embeddable(self):
        response = self._publish_and_verify(SIMPLE_HTML)
        ok_('X-Frame-Options' not in response)

    def test_void_content_is_rejected(self):
        response = self.client.post('/api/page', {'html': ''})
        eq_(response.status_code, 400)
        eq_(response.content, "HTML body expected.")

    @mock.patch('webpagemaker.api.decorators.cache', FakeCache)
    def test_publishing_is_rate_limited(self):
        FakeCache.keys.clear()
        response = self.client.post('/api/page', {'html': 'hi'})
        eq_(response.status_code, 200)
        eq_(len(FakeCache.keys), 1)
        timeout = FakeCache.keys.values()[0]['timeout']
        ok_(timeout >= 1, 'cache timeout is at least 1s')
        response = self.client.post('/api/page', {'html': 'hi again'})
        eq_(response.status_code, 403)
        eq_(response.content, 'Sorry, you can only publish a page every' +
                              ' %d seconds, try again in a bit' % timeout)

    def test_retrieving_page_delivers_x_robots_tag(self):
        response = self._publish_and_verify(SIMPLE_HTML)
        eq_(response['X-Robots-Tag'], "noindex, nofollow")
		
    def test_retrieving_page_delivers_cache_headers(self):
        response = self._publish_and_verify(SIMPLE_HTML)
        eq_(response['Cache-Control'], "public, max-age=%s" % views.CACHE_LIFETIME)
        eq_(response['ETag'], views.generate_etag(SIMPLE_HTML))
    
    
    def test_publishing_ascii_works(self):
        self._publish_and_verify(SIMPLE_HTML)

    def test_publishing_utf8_works(self):
        HTML = u"<!DOCTYPE html><html><head><meta charset=\"utf-8\">" + \
               u"<title>hi</title></head>" + \
               u"<body>hello\u2026</body></html>"
        self._publish_and_verify(HTML.encode("utf-8"))

    def test_edit_url_returns_200(self):
        url = self.client.post('/api/page', {'html': 'hi'}).content
        response = self.client.get('%sedit' % url)
        eq_(response.status_code, 200)
