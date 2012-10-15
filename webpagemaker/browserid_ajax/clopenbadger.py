import time
import math

from django.conf import settings
import jwt

def create_token_from_request(request, default=None):
    if request.user.is_authenticated():
        return create_token(request.user.email)
    return default

def create_token(email):
    # See https://github.com/mozilla/clopenbadger/wiki/API
    claims = {
        "iss": settings.SITE_URL,
        "aud": settings.CLOPENBADGER_URL,
        "prn": email,
        "exp": math.floor(time.time()) + settings.CLOPENBADGER_TOKEN_LIFETIME
    }
    return jwt.encode(claims, settings.CLOPENBADGER_SECRET)
