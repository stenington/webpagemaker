"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory
from nose.tools import eq_, ok_
import jingo

from . import views

class SimpleTest(TestCase):
    def test_editor_returns_200(self):
        response = self.client.get('/en-US/editor')
        eq_(response.status_code, 200)
        
    def test_remix_returns_200(self):
        response = self.client.get('/p/abcdefg1234/edit')
        eq_(response.status_code, 200)
        self.assertTrue('/p/abcdefg1234' in response.content)
        
    def test_deployment_type(self):
        # TODO: Eventually, we should just use the @patch decorator
        # from the 'mock' package for this.
        orig = settings.DEV

        try:
            settings.DEV = True
            response = self.client.get('/en-US/editor')
            ok_('deployment-type-development' in response.content)

            settings.DEV = False
            response = self.client.get('/en-US/editor')
            ok_('deployment-type-production' in response.content)
        finally:
            settings.DEV = orig

    def test_editor_template(self):
        factory = RequestFactory()
        request = factory.get('/en-US/editor')
        ctx = {
            'remix_url': 'I_AM_A_REMIX_URL',
            'PUBLISH_URL': 'I_AM_A_PUBLISH_URL',
            'REMIX_URL_TEMPLATE': 'I_AM_A_REMIX_URL_TEMPLATE'
        }
        response = jingo.render(request, "editor/editor.html", ctx)
        self.assertTrue("I_AM_A_REMIX_URL" in response.content)
        self.assertTrue("I_AM_A_PUBLISH_URL" in response.content)
        self.assertTrue("I_AM_A_REMIX_URL_TEMPLATE" in response.content)
