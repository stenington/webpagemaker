import time
import math
import urlparse

from django.conf import settings
import jwt

DEFAULT_PORTS = {
    'http': 80,
    'https': 443
}

def create_token_from_request(request, default=None):
    if request.user.is_authenticated():
        return create_token(request.user.email)
    return default

def normalize_url(url):
    parts = urlparse.urlsplit(url)
    netloc = parts.netloc
    if ':' not in netloc:
        netloc = '%s:%d' % (netloc, DEFAULT_PORTS[parts.scheme])
    return urlparse.urlunsplit((parts.scheme, netloc, parts.path,
                                parts.query, parts.fragment))

def create_token(email):
    # See https://github.com/mozilla/clopenbadger/wiki/API
    claims = {
        "iss": settings.SITE_URL,
        "aud": normalize_url(settings.CLOPENBADGER_URL),
        "prn": email,
        "exp": math.floor(time.time()) + settings.CLOPENBADGER_TOKEN_LIFETIME
    }
    return jwt.encode(claims, settings.CLOPENBADGER_SECRET)
