from django.conf import settings
from django.core.urlresolvers import reverse
import jingo

def _editor(request, remix_url):
    ctx = {
        'remix_url': remix_url,
        'PUBLISH_URL': request.build_absolute_uri("/")[:-1],
        'REMIX_URL_TEMPLATE': request.build_absolute_uri("/")[:-1] +
                              "{{VIEW_URL}}/edit"
    }
    if settings.DEV:
        ctx['DEPLOYMENT_TYPE'] = 'development'
    else:
        ctx['DEPLOYMENT_TYPE'] = 'production'
    return jingo.render(request, "editor/editor.html", ctx)
    
def default_editor(request):
    return _editor(request,
                   '%sfriendlycode/default-content.html' % settings.MEDIA_URL)

def editor(request, **kwargs):
    viewname = kwargs['remix']
    del kwargs['remix']
    to_remix = reverse(viewname, kwargs=kwargs)
    return _editor(request, to_remix)
