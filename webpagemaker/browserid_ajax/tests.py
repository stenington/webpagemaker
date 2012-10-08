from django.utils import simplejson as json
import test_utils
from nose.tools import eq_, ok_
import mock

def fake_verify_failure(assertion, audience):
    return False

def fake_verify_success(assertion, audience):
    return {
        'status': 'okay',
        'email': assertion
    }

def ensure_status_has_csrf_token(status):
    eq_(type(status['csrfToken']), unicode)
    ok_(len(status['csrfToken']))

class BrowseridAjaxTests(test_utils.TestCase):
    def test_status_works(self):
        response = self.client.get('/browserid/status')
        eq_(response.status_code, 200)
        eq_(response['Content-Type'], 'application/json')
        status = json.loads(response.content)
        eq_(status['email'], None)
        ensure_status_has_csrf_token(status)
        
    def test_logout_redirects_to_status(self):
        response = self.client.post('/browserid/logout')
        eq_(response.status_code, 302)
        eq_(response['Location'], 'http://testserver/browserid/status')

    def test_verify_fails_with_no_assertion(self):
        response = self.client.post('/browserid/verify')
        eq_(response.status_code, 400)
        eq_(response.content, 'assertion required')
    
    @mock.patch('django_browserid.auth.verify', fake_verify_failure)
    def test_verify_fails_with_bad_assertion(self):
        response = self.client.post('/browserid/verify', {
            'assertion': 'lol'
        })
        eq_(response.status_code, 400)
        eq_(response.content, 'bad assertion')
    
    @mock.patch('django_browserid.auth.verify', fake_verify_success)
    def test_verify_succeeds_with_good_assertion(self):
        response = self.client.post('/browserid/verify', {
            'assertion': 'foo@bar.org'
        }, follow=True)
        eq_(response.status_code, 200)
        status = json.loads(response.content)
        eq_(status['email'], 'foo@bar.org')
        ensure_status_has_csrf_token(status)
