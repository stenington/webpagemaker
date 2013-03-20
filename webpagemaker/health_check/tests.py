import base64
import json
import test_utils
from nose.tools import eq_, ok_
import mock

from .views import health_check

hi_auth = 'basic %s' % base64.b64encode('health_check:hi')

class WithoutAuthTests(test_utils.TestCase):
    @mock.patch('django.conf.settings.HEALTH_CHECK_PASSWORD', None)
    def test_returns_501_without_elb_arg_but_no_password_is_set(self):
        response = self.client.get('/health_check')
        eq_(response.status_code, 501)

    @mock.patch('django.conf.settings.HEALTH_CHECK_PASSWORD', 'hi')
    def test_returns_401_without_elb_arg(self):
        response = self.client.get('/health_check')
        eq_(response.status_code, 401)
        eq_(response['WWW-Authenticate'], 'Basic realm="health_check"')

    def test_returns_200_with_elb_arg(self):
        response = self.client.get('/health_check?elb=true')
        eq_(response.status_code, 200)
        eq_(response['Content-Type'], 'application/json')
        eq_(response.content, '{"status": "OK"}')

class WithBadAuthTests(test_utils.TestCase):
    @mock.patch('django.conf.settings.HEALTH_CHECK_PASSWORD', 'hi')
    def test_returns_401_when_auth_header_is_lol(self):
        response = self.client.get('/health_check',
                                   HTTP_AUTHORIZATION='lol')
        eq_(response.status_code, 401)

    @mock.patch('django.conf.settings.HEALTH_CHECK_PASSWORD', 'hi')
    def test_returns_401_when_auth_header_is_digest(self):
        response = self.client.get('/health_check',
                                   HTTP_AUTHORIZATION='digest wut')
        eq_(response.status_code, 401)

    @mock.patch('django.conf.settings.HEALTH_CHECK_PASSWORD', 'hi')
    def test_returns_401_when_auth_header_creds_are_not_b64encoded(self):
        response = self.client.get('/health_check',
                                   HTTP_AUTHORIZATION='basic lol')
        eq_(response.status_code, 401)

    @mock.patch('django.conf.settings.HEALTH_CHECK_PASSWORD', 'hi')
    def test_returns_401_when_auth_header_creds_do_not_split(self):
        response = self.client.get('/health_check',
                                   HTTP_AUTHORIZATION='basic bG9s')
        eq_(response.status_code, 401)

    @mock.patch('django.conf.settings.HEALTH_CHECK_PASSWORD', 'hi')
    def test_returns_401_when_auth_header_username_is_not_correct(self):
        creds = base64.b64encode('somebody:badpassword')
        response = self.client.get('/health_check',
                                   HTTP_AUTHORIZATION='basic %s' % creds)
        eq_(response.status_code, 401)

    @mock.patch('django.conf.settings.HEALTH_CHECK_PASSWORD', 'hi')
    def test_returns_401_when_auth_header_password_is_not_correct(self):
        creds = base64.b64encode('health_check:badpassword')
        response = self.client.get('/health_check',
                                   HTTP_AUTHORIZATION='basic %s' % creds)
        eq_(response.status_code, 401)

class WithGoodAuthTests(test_utils.TestCase):
    @mock.patch('django.contrib.auth.models.User.objects', None)
    @mock.patch('django.conf.settings.HEALTH_CHECK_PASSWORD', 'hi')
    def test_returns_500_when_something_is_wrong(self):
        response = self.client.get('/health_check',
                                   HTTP_AUTHORIZATION=hi_auth)
        eq_(response.status_code, 500)
        info = json.loads(response.content)
        eq_(response['Content-Type'], 'application/json')
        eq_(info['status'], 'FAILED')
        eq_(info['database']['online'], None)

    @mock.patch('django.conf.settings.HEALTH_CHECK_PASSWORD', 'hi')
    def test_returns_200_when_all_is_well(self):
        response = self.client.get('/health_check',
                                   HTTP_AUTHORIZATION=hi_auth)
        eq_(response.status_code, 200)
        info = json.loads(response.content)
        eq_(response['Content-Type'], 'application/json')
        eq_(info['status'], 'OK')
        eq_(info['database']['online'], True)
        eq_(type(info['timezone']), unicode)
