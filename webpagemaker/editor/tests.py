"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from nose.tools import eq_, ok_

from . import views

class SimpleTest(TestCase):
    def test_blank_page(self):
        response = self.client.get('/en-US/editor/blank')
        eq_(response.status_code, 200)
        ok_('x-frame-options' not in response) 
        
    def test_editor(self):
        response = self.client.get('/en-US/editor')
        eq_(response.status_code, 200)
        
    def test__frontend_html(self):
        html = views._frontend_html(base_url="BASE243", publish_url="PUB324",
                                    blank_url="BLANK591", remix_url="BLE24")
        self.assertTrue("PUB324" in html)
        self.assertTrue("BASE243" in html)
        self.assertTrue("BLANK591" in html)
        self.assertTrue("BLE24" in html)
        
    def test__sub_base_href(self):
        html = views._sub_base_href('\n  <base href="foibles.">\n\n', 'baseurl')
        self.assertEqual(html, '\n  <base href="baseurl">\n\n')

    def test__sub_remix_href(self):
        html = views._sub_remix_url('\n<meta name="remix-url" content="use-querystring">', 'remurl')
        self.assertEqual(html, '\n<meta name="remix-url" content="remurl">')
    
    def test__sub_publish_url(self):
        html = views._sub_publish_url('\n<meta name="publish-url" content="blarg">', 'puburl')
        self.assertEqual(html, '\n<meta name="publish-url" content="puburl">')
