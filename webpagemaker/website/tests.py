from django.test import TestCase
from nose.tools import eq_

class SmokeTest(TestCase):
    def test_home_page(self):
        response = self.client.get('/en-US/projects')
        eq_(response.status_code, 200)
    
    def test_projects_page(self):
        response = self.client.get('/en-US/projects')
        eq_(response.status_code, 200)
    
    def test_gallery_page(self):
        response = self.client.get('/en-US/gallery')
        eq_(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get('/en-US/about')
        eq_(response.status_code, 200)
    
    def test_webarcade_page(self):
        response = self.client.get('/en-US/webarcade')
        eq_(response.status_code, 200)
    
    