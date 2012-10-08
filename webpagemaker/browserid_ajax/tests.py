from django.utils import simplejson as json
import test_utils
from nose.tools import eq_, ok_

class AjaxTests(test_utils.TestCase):
    def test_status_works_when_logged_out(self):
        response = self.client.get('/browserid/status')
        eq_(response.status_code, 200)
        eq_(response['Content-Type'], 'application/json')
        status = json.loads(response.content)
        eq_(status['email'], None)
        eq_(type(status['csrfToken']), unicode)
        ok_(len(status['csrfToken']))
        