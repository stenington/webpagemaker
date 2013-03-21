from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings
from django.contrib.auth.models import User

import json, base64

HEALTH_CHECK_USERNAME = 'health_check'
HEALTH_CHECK_REALM = 'health_check'

def is_http_basic_auth_correct(request, expected_username, expected_password):
    if not 'HTTP_AUTHORIZATION' in request.META:
        return False

    auth = request.META['HTTP_AUTHORIZATION'].split()
    if len(auth) != 2:
        return False

    if auth[0].lower() != "basic":
        return False

    uname = None
    passwd = None

    try:
        uname, passwd = base64.b64decode(auth[1]).split(':')
    except Exception:
        return False

    if not (uname == expected_username and passwd == expected_password):
        return False

    return True

def calculate_overall_status(data):
    overall_status = "OK"
    for key in data:
        if not data[key]:
            overall_status = "FAILED"
        if type(data[key]) == dict:
            overall_status = calculate_overall_status(data[key])
    return overall_status

def health_check(request):
    if request.GET.get('elb', '') == 'true':
        return HttpResponse('{"status": "OK"}', mimetype='application/json')

    # See if they provided login credentials.

    if not settings.HEALTH_CHECK_PASSWORD:
        response = HttpResponse()
        response.status_code = 501
        return response

    if not is_http_basic_auth_correct(request, HEALTH_CHECK_USERNAME,
                                      settings.HEALTH_CHECK_PASSWORD):
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="%s"' % HEALTH_CHECK_REALM
        return response

    # default data, None means the parameter hasn't been checked yet
    data    =   {
        'database': {
            'online': None
        },
        'timezone': getattr(settings, 'TIME_ZONE', None),
    }
    
    # connect to the database, getting a user or a User.DoesNotExist
    # exception means the database is online
    try:
        User.objects.latest('pk')
        data['database']['online'] = True
    except User.DoesNotExist:
        data['database']['online'] = True
    except Exception:
        pass
        
    data['status'] = calculate_overall_status(data)
    
    response = HttpResponse
    if not data['status'] == "OK":
        response = HttpResponseServerError
    return response(json.dumps(data), mimetype='application/json')
