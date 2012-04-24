from django.conf import settings

import test_utils
from nose.tools import eq_

class PublishTests(test_utils.TestCase):
    def test_massive_content_is_rejected(self):
        massive_content = "*" * (settings.MAX_PUBLISHED_PAGE_SIZE + 1)
        response = self.client.post('/api/page', data=massive_content,
                                    content_type="text/html")
        eq_(response.status_code, 413)
        eq_(response.content, "Request Entity Too Large")

    def test_no_content_is_rejected(self):
        response = self.client.post('/api/page', data="",
                                    content_type="text/html")
        eq_(response.status_code, 400)
        eq_(response.content, "HTML body expected.")

    def test_publish(self):
        HTML = "<!DOCTYPE html><html><head><title>hi</title></head>" + \
               "<body>hello.</body></html>"
        response = self.client.post('/api/page', data=HTML,
                                    content_type="text/html")
        eq_(response.status_code, 200)
        eq_(response['Access-Control-Allow-Origin'], '*')

        page_id = response.content
        response = self.client.get(page_id)
        eq_(response.status_code, 200)
        eq_(response['Access-Control-Allow-Origin'], '*')
        eq_(response['Content-Type'], 'text/html; charset=utf-8')
        eq_(response.content, HTML)
