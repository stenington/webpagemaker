from django.http import HttpResponse, HttpResponseBadRequest, \
                        HttpResponseRedirect
from django.contrib import auth
from django.views.decorators.http import require_POST
from session_csrf import anonymous_csrf
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

from django_browserid.base import get_audience

@anonymous_csrf
def get_status(request):
    email = None
    if request.user.is_authenticated():
        email = request.user.email
    data = {
      'email': email,
      'csrfToken': request.csrf_token
    }
    return HttpResponse(json.dumps(data), mimetype="application/json")

@require_POST
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse(get_status))

@require_POST
def verify(request):
    if not 'assertion' in request.POST:
        return HttpResponseBadRequest('need an assertion, bro.')

    assertion = request.POST['assertion']
    audience = get_audience(request)
    user = auth.authenticate(assertion=assertion, audience=audience)

    if user and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect(reverse(get_status))
    else:
        return HttpResponseBadRequest('bad assertion, bro.')
