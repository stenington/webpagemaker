import warnings
from django.utils import simplejson as json
from django.conf import settings
import test_utils
from nose.tools import eq_, ok_
import mock
import jwt

DEFAULT_SETTINGS = {
    'SITE_URL': 'http://localhost:8000',
    'CLOPENBADGER_URL': 'https://clopenbadger.org',
    'CLOPENBADGER_SECRET': 'seekret',
}

for setting in DEFAULT_SETTINGS:
    if not hasattr(settings, setting):
        warnings.warn("local setting %s is undefined." % setting)
        setattr(settings, setting, DEFAULT_SETTINGS[setting])
del setting

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

class ClopenbadgerTokenTests(test_utils.TestCase):
    def test_no_token_provided_when_logged_out(self):
        response = self.client.get('/browserid/status')
        status = json.loads(response.content)
        eq_(status['clopenbadgerToken'], None)

    @mock.patch('django_browserid.auth.verify', fake_verify_success)
    @mock.patch('time.time', lambda: 5)
    def test_token_provided_when_logged_in(self):
        response = self.client.post('/browserid/verify', {
            'assertion': 'foo@bar.org'
        }, follow=True)
        status = json.loads(response.content)
        token = status['clopenbadgerToken'].encode('ascii')
        claims = jwt.decode(token, settings.CLOPENBADGER_SECRET)
        eq_(claims['iss'], settings.SITE_URL)
        eq_(claims['aud'], settings.CLOPENBADGER_URL)
        eq_(claims['prn'], 'foo@bar.org')
        eq_(claims['exp'], 5 + settings.CLOPENBADGER_TOKEN_LIFETIME)

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
