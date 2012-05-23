import os
import re

from django.http import HttpResponse
from django.conf import settings
from django.core.urlresolvers import reverse

def _sub_base_href(html, base_url):
    return re.sub(r'<base href=".*">', '<base href="%s">' % base_url, html)

def _sub_publish_url(html, publish_url):
    return re.sub(r'<meta name="publish-url" content=".*">',
                  '<meta name="publish-url" content="%s">' % publish_url,
                  html)

def _sub_remix_url(html, remix_url):
    return re.sub(r'<meta name="remix-url" content=".*">',
                  '<meta name="remix-url" content="%s">' % remix_url,
                  html)

def _frontend_html(base_url, publish_url, blank_url, remix_url):
    mydir = os.path.dirname(__file__)
    html = open(os.path.join(mydir, 'friendlycode', 'index.html')).read()
    html = html.replace("blank.html", blank_url)
    html = _sub_remix_url(html, remix_url)
    return _sub_base_href(_sub_publish_url(html, publish_url), base_url)

def _editor(request, remix_url):
    return HttpResponse(_frontend_html(
        base_url='%sfriendlycode/' % settings.MEDIA_URL,
        publish_url=request.build_absolute_uri("/")[:-1],
        blank_url=request.build_absolute_uri(reverse(blank_page)),
        remix_url=remix_url
        ))

BLANK_HTML = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Blank Page</title>
  </head>
  <body>
  </body>
</html>"""

def default_editor(request):
    return _editor(request, 'use-querystring')

def blank_page(request):
    response = HttpResponse(BLANK_HTML)
    response.no_frame_options = True
    return response

def editor(request, **kwargs):
    viewname = kwargs['remix']
    del kwargs['remix']
    to_remix = reverse(viewname, kwargs=kwargs)
    return _editor(request, to_remix)
