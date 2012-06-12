import os
import re

from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse

class memoize(object):
    """
    Cache the results of a function only if settings.DEV is False
    """
    contents = None
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        def inner(*args):
            if not self.contents or settings.DEV:
                self.contents = self.func(*args)
            return self.contents
        return inner(*args)

@memoize
def _friendly_code_html():
    mydir = os.path.dirname(__file__)
    index_file = os.path.join(mydir, 'friendlycode', 'index.html')
    with open(index_file) as f:
        return f.read()
    
def _sub_meta(html, meta_name, replacement):
    return _subvar(html, r'<meta name="' + meta_name + r'" content=".*">',
                   replacement)
    
def _subvar(html, template, replacement):
    regexp = "(%s)(.*)(%s)" % tuple(template.split(".*"))
    return re.sub(regexp, r'\1' + replacement + r'\3', html)

def _sub_base_href(html, base_url):
    return _subvar(html, r'<base href=".*">', base_url)

def _sub_publish_url(html, publish_url):
    return _sub_meta(html, 'publish-url', publish_url)

def _sub_remix_url(html, remix_url):
    return _sub_meta(html, 'remix-url', remix_url)

def _sub_deployment_type(html):
    if settings.DEV:
        deployment_type = 'development'
    else:
        deployment_type = 'production'
    return _sub_meta(html, 'deployment-type', deployment_type)

def _frontend_html(base_url, publish_url, remix_url):
    html = _friendly_code_html()
    html = _sub_remix_url(html, remix_url)
    html = _sub_base_href(_sub_publish_url(html, publish_url), base_url)
    return _sub_deployment_type(html)

def _editor(request, remix_url):
    rel_base_url = '%sfriendlycode/' % settings.MEDIA_URL
    return HttpResponse(_frontend_html(
        base_url=request.build_absolute_uri(rel_base_url),
        publish_url=request.build_absolute_uri("/")[:-1],
        remix_url=remix_url
        ))

def default_editor(request):
    return _editor(request,
                   '%sfriendlycode/default-content.html' % settings.MEDIA_URL)

def editor(request, **kwargs):
    viewname = kwargs['remix']
    del kwargs['remix']
    to_remix = reverse(viewname, kwargs=kwargs)
    return _editor(request, to_remix)
