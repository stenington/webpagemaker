from django.conf import settings

import test_utils
from nose.tools import eq_

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
        response = self.client.post('/api/page', data=html,
                                    content_type="text/html")
        eq_(response.status_code, 200)
        eq_(response['Access-Control-Allow-Origin'], '*')

        page_id = response.content
        response = self.client.get(page_id)
        eq_(response.status_code, 200)
        eq_(response['Access-Control-Allow-Origin'], '*')
        eq_(response['Content-Type'], 'text/html; charset=utf-8')
        eq_(type(response.content), str)
        eq_(response.content, expected_html)

    def test_massive_content_is_rejected(self):
        massive_content = "*" * (settings.MAX_PUBLISHED_PAGE_SIZE + 1)
        response = self.client.post('/api/page', data=massive_content,
                                    content_type="text/html")
        eq_(response.status_code, 413)
        eq_(response.content, "Request Entity Too Large")

    def test_void_content_is_rejected(self):
        response = self.client.post('/api/page', data="",
                                    content_type="text/html")
        eq_(response.status_code, 400)
        eq_(response.content, "HTML body expected.")

    def test_publishing_ascii_works(self):
        HTML = "<!DOCTYPE html><html><head><title>hi</title></head>" + \
               "<body>hello.</body></html>"
        self._publish_and_verify(HTML)

    def test_publishing_utf8_works(self):
        HTML = u"<!DOCTYPE html><html><head><meta charset=\"utf-8\">" + \
               u"<title>hi</title></head>" + \
               u"<body>hello\u2026</body></html>"
        self._publish_and_verify(HTML.encode("utf-8"))
