from django.conf import settings
from django.utils import simplejson as json

import test_utils
from nose.tools import eq_, ok_

SIMPLE_HTML = "<!DOCTYPE html><html><head><title>hi</title></head>" + \
              "<body>hello.</body></html>"

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
    
    def test_origin_url_is_returned(self):
        response = self.client.post('/api/page', {
          'html': 'hi',
          'original-url': 'http://blah.com/'
          })
        response = self.client.get(response.content)
        eq_(response['x-original-url'], 'http://blah.com/')

    def test_void_content_is_rejected(self):
        response = self.client.post('/api/page', {'html': ''})
        eq_(response.status_code, 400)
        eq_(response.content, "HTML body expected.")

    def test_retrieving_page_delivers_x_robots_tag(self):
    	response = self._publish_and_verify(SIMPLE_HTML)
    	eq_(response['X-Robots-Tag'], "noindex, nofollow")
		
    def test_publishing_ascii_works(self):
        self._publish_and_verify(SIMPLE_HTML)

    def test_publishing_utf8_works(self):
        HTML = u"<!DOCTYPE html><html><head><meta charset=\"utf-8\">" + \
               u"<title>hi</title></head>" + \
               u"<body>hello\u2026</body></html>"
        self._publish_and_verify(HTML.encode("utf-8"))
