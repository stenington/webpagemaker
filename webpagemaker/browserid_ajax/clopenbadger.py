import time
import math

from django.conf import settings
import jwt

def create_token(email):
    # See https://github.com/mozilla/clopenbadger/wiki/API
    claims = {
        "iss": settings.SITE_URL,
        "aud": settings.CLOPENBADGER_URL,
        "prn": email,
        "exp": math.floor(time.time()) + settings.CLOPENBADGER_TOKEN_LIFETIME
    }
    return jwt.encode(claims, settings.CLOPENBADGER_SECRET)
