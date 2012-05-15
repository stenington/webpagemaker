"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from . import views

class SimpleTest(TestCase):
    def test__frontend_html(self):
        html = views._frontend_html(base_url="BASE243", publish_url="PUB324",
                                    blank_url="BLANK591")
        self.assertTrue("PUB324" in html)
        self.assertTrue("BASE243" in html)
        self.assertTrue("BLANK591" in html)
        
    def test__sub_base_href(self):
        html = views._sub_base_href('\n  <base href="foibles.">\n\n', 'baseurl')
        self.assertEqual(html, '\n  <base href="baseurl">\n\n')

    def test__sub_publish_url(self):
        html = views._sub_publish_url('\n<meta name="publish-url" content="blarg">', 'puburl')
        self.assertEqual(html, '\n<meta name="publish-url" content="puburl">')
