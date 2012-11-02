import re

from django.conf import settings
from django.test.client import RequestFactory
from nose.tools import eq_, ok_
import test_utils

from . import views
from .management.commands.slurplearningprojects import rebase_static_urls

def test_make_context_works_with_non_absolute_uri():
    req = RequestFactory().get('/')
    ctx = views._make_context(req, '/blarg/')
    eq_(ctx['HTTP_STATIC_URL'], 'http://testserver/blarg/')

def test_make_context_works_with_absolute_uri():
    req = RequestFactory().get('/')
    ctx = views._make_context(req, 'http://u/blarg/')
    eq_(ctx['HTTP_STATIC_URL'], 'http://u/blarg/')

class RebaseStaticUrlsTests(test_utils.TestCase):
    def test_replaces_relative_urls(self):
        eq_(rebase_static_urls('static/foo', 'BLARG/'), 'BLARG/foo')

    def test_replaces_multiple_times(self):
        eq_(rebase_static_urls('static/foo static/bar', 'BLAP/'),
            'BLAP/foo BLAP/bar')
    
    def test_ignores_non_relative_static_urls(self):
        eq_(rebase_static_urls('/static/foo', 'BINGY/'), '/static/foo')

class RenderTests(test_utils.TestCase):
    def test_http_static_includes_protocol(self):
        response = self.client.get('/en-US/projects/tests')
        info = eval(response.content)
        ok_(re.match(r'^https?:\/\/.+', info['HTTP_STATIC_URL']))

    def test_404_returned_for_nonexistent_projects(self):
        response = self.client.get('/en-US/projects/nonexistent')
        eq_(response.status_code, 404)

    def test_200_returned_for_existing_projects(self):
        response = self.client.get('/en-US/projects/meme')
        eq_(response.status_code, 200)

    def test_200_returned_for_editing_existing_projects(self):
        response = self.client.get('/en-US/projects/meme/edit')
        eq_(response.status_code, 200)
        
    def test_cors_is_supported(self):
        response = self.client.get('/en-US/projects/meme')
        eq_(response['Access-Control-Allow-Origin'], '*')
