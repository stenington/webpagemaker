import test_utils
from nose.tools import eq_

from webpagemaker.api.views import BLOCKED_MSG

SIMPLE_HTML = "<!DOCTYPE html><html><head><title>hi</title></head>" + \
              "<body>hello.</body></html>"

class BrowserBlockingTests(test_utils.TestCase):

    def _request_published_page_as(self, user_agent):
        response = self.client.post('/api/page', {'html': SIMPLE_HTML})
        page_id = response.content
        response = self.client.get(page_id, HTTP_USER_AGENT=user_agent)
        return response


    def test_known_problem_browsers_cannot_see_published_pages(self):
        # TODO: Do we want a (semi-)comprehensive list of problem browsers?
        for user_agent in ['MSIE 1', 'MSIE 1;', 'MSIE 2.0', 'MSIE 3.1', 
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1;']:
            response = self._request_published_page_as(user_agent)
            eq_(response.status_code, 200)
            eq_(response.content, BLOCKED_MSG)

    def test_good_browsers_should_see_published_page(self):
        for user_agent in ['MSIE 8.0', 'MSIE 10', 'Mozilla 5.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1;']:
            response = self._request_published_page_as(user_agent)
            eq_(response.status_code, 200)
            eq_(response.content, SIMPLE_HTML)
      
