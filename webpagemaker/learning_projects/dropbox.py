import urllib2

from django.conf.urls.defaults import patterns
from django.conf import settings
from django.http import HttpResponse

def render_dropbox_static(request, name, path):
    """
    Render a static resource that proxies to the file server that
    in-development learning projects are being created on.
    
    This view is for development and debugging purposes ONLY.
    """
    
    url = '%s%s/static/%s' % (settings.LEARNING_PROJECTS_DROPBOX_URL,
                              name, path)
    try:
        f = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        return HttpResponse(content="alas, %d." % e.code, status=e.code)
    except Exception:
        return HttpResponseBadRequest('something terrible happened')
    
    response = HttpResponse(
        f, # Hopefully we are iterating over this.
        content_type=f.info()['content-type']
        )
    response['Access-Control-Allow-Origin'] = '*'
    return response

def render_dropbox_project(request, name):
    """
    Render a learning project's HTML that proxies to the file server that
    in-development learning missions are being created on, rewriting
    links to static content so that they point to our proxied static
    resources.
    
    This view is for development and debugging purposes ONLY.
    """
    
    url = '%s%s/%s.html' % (settings.LEARNING_PROJECTS_DROPBOX_URL,
                            name, name)
    try:
        f = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        return HttpResponse(content="alas, %d." % e.code, status=e.code)
    html = f.read()
    static_base = request.build_absolute_uri('/dropbox/%s/' % name)
    html = html.replace('static/', static_base)
    response = HttpResponse(html)
    response['Access-Control-Allow-Origin'] = '*'
    return response

urlpatterns = patterns('',
    (r'^dropbox/(?P<name>[A-Za-z0-9\-_]+)/(?P<path>.*)$',
      render_dropbox_static),
    (r'^projects/dropbox/(?P<name>[A-Za-z0-9\-_]+)$',
      render_dropbox_project)
)
