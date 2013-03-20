from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache

import os, json, random, string, base64
from datetime import datetime

HEALTH_CHECK_USERNAME = 'health_check'
HEALTH_CHECK_REALM = 'health_check'

def ask_for_auth():
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="%s"' % HEALTH_CHECK_REALM
    return response

def health_check(request):
    if request.GET.get('elb', '') == 'true':
        return HttpResponse('{"status": "OK"}', mimetype = 'application/json')

    # See if they provided login credentials.

    if not settings.HEALTH_CHECK_PASSWORD:
        response = HttpResponse()
        response.status_code = 501
        return response

    if not 'HTTP_AUTHORIZATION' in request.META:
        return ask_for_auth()

    auth = request.META['HTTP_AUTHORIZATION'].split()
    if len(auth) != 2:
        return ask_for_auth()

    # NOTE: We are only support basic authentication for now.
    if auth[0].lower() != "basic":
        return ask_for_auth()

    uname = None
    passwd = None

    try:
        uname, passwd = base64.b64decode(auth[1]).split(':')
    except Exception:
        return ask_for_auth()

    if not (uname == HEALTH_CHECK_USERNAME and
            passwd == settings.HEALTH_CHECK_PASSWORD):
        return ask_for_auth()

    # default data, None means the parameter hasn't been checked yet
    data    =   {
        'status':       None,
        'database': {
            'online':   None
        },
        'timezone':     getattr(settings, 'TIME_ZONE', None),
    }
    
    # connect to the database, getting a user or a User.DoesNotExist
    # exception means the database is online
    try:
        User.objects.latest('pk')
        data['database']['online']  =   True
    except User.DoesNotExist:
        data['database']['online']  =   True
    except Exception:
        pass
        
    overall_status  =   "OK"
    for key in data:
        if key == 'status':
            continue
        if not data[key]:
            overall_status  =   "FAILED"
        if type(data[key]) == dict:
            for k in data[key]:
                if not data[key][k]:
                    overall_status  =   "FAILED"
    data['status']  =   overall_status
    
    response    =   HttpResponse
    if not data['status'] == "OK":
        response    =   HttpResponseServerError
    return response(json.dumps(data), mimetype = 'application/json')
