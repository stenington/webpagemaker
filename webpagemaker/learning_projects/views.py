from django.http import HttpResponseNotFound
from django.conf import settings
from jinja2 import TemplateNotFound
import jingo

def _make_context(request, static_url):
    ctx = {}
    if static_url.startswith('/'):
        ctx['HTTP_STATIC_URL'] = request.build_absolute_uri(static_url)
    else:
        ctx['HTTP_STATIC_URL'] = static_url
    return ctx
    
def render(request, name):
    template = "learning_projects/%s.html" % name
    ctx = _make_context(request, settings.STATIC_URL)
    try:
        response = jingo.render(request, template, ctx)
    except TemplateNotFound:
        response = HttpResponseNotFound('could not find %s' % name)
    response['Access-Control-Allow-Origin'] = '*'
    return response
