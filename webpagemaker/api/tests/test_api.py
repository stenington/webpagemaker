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

    def _publish_and_verify_body(self, body, expected_body):
        """
        Like _publish_and_verify, but takes the content of a
        <body> element and wraps it in an HTML5 document for us.
        """
        
        before = "<!DOCTYPE html><html><head></head><body>"
        after = "</body></html>"
        self._publish_and_verify(before + body + after,
                                 before + expected_body + after)

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

    def test_javascript_attributes_are_stripped(self):
        self._publish_and_verify_body(body='<a onclick="foo()">u</a>',
                                      expected_body="<a>u</a>")

    def test_javascript_links_are_stripped(self):
        self._publish_and_verify_body(body='<a href="javascript:foo()">u</a>',
                                      expected_body="<a>u</a>")
        
    def test_script_tags_are_stripped(self):
        self._publish_and_verify_body(body="<script>alert('yo');</script>",
                                      expected_body="alert('yo');")
