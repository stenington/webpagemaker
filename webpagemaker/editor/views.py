from session_csrf import anonymous_csrf
from django.conf import settings
from django.core.urlresolvers import reverse
import jingo

from webpagemaker.browserid_ajax import clopenbadger

def _editor(request, remix_url):
    ctx = {
        'remix_url': remix_url,
        'clopenbadger_token': clopenbadger.create_token_from_request(
            request=request,
            default=''
        ),
        'CLOPENBADGER_URL': settings.CLOPENBADGER_URL,
        'PUBLISH_URL': request.build_absolute_uri("/")[:-1],
        'REMIX_URL_TEMPLATE': request.build_absolute_uri("/")[:-1] +
                              "{{VIEW_URL}}edit"
    }
    if settings.CLOPENBADGER_URL == "http://fake-clopenbadger":
        ctx['USE_FAKE_CLOPENBADGER'] = True
    if settings.DEV:
        ctx['DEPLOYMENT_TYPE'] = 'development'
    else:
        ctx['DEPLOYMENT_TYPE'] = 'production'
    return jingo.render(request, "editor/editor.html", ctx)
    
@anonymous_csrf
def default_editor(request):
    return _editor(request, '%sfriendlycode/templates/default-content.html' %
                             settings.MEDIA_URL)

@anonymous_csrf
def editor(request, **kwargs):
    viewname = kwargs['remix']
    del kwargs['remix']
    to_remix = reverse(viewname, kwargs=kwargs)
    return _editor(request, to_remix)
