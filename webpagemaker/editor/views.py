import os
import re

from django.http import HttpResponse
from django.conf import settings

def _sub_base_href(html, base_url):
    return re.sub(r'<base href=".*">', '<base href="%s">' % base_url, html)

def _sub_publish_url(html, publish_url):
    return re.sub(r'<meta name="publish-url" content=".*">',
                  '<meta name="publish-url" content="%s">' % publish_url,
                  html)

def _frontend_html(base_url, publish_url):
    mydir = os.path.dirname(__file__)
    html = open(os.path.join(mydir, 'friendlycode', 'index.html')).read()
    return _sub_base_href(_sub_publish_url(html, publish_url), base_url)
    
def editor(request):
    return HttpResponse(_frontend_html(
        base_url='%sfriendlycode/' % settings.MEDIA_URL,
        publish_url=request.build_absolute_uri("/")[:-1]
        ))
