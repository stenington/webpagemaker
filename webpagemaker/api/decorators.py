from django.core.cache import cache
from django.http import HttpResponseBadRequest, HttpResponseForbidden
import hashlib

def throttle_view(func, methods=None, duration=30):
    def inner(request, *args, **kwargs):
        throttled_methods = methods if methods else ['POST', 'GET']
        if request.method in throttled_methods:
            remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or \
                          request.META.get('REMOTE_ADDR')
            key = (hashlib.md5('%s.%s' % (remote_addr, request.path_info))
                   .hexdigest())
            if cache.get(key):
                return HttpResponseForbidden('Please try again later.')
            else:
                cache.set(key, True, duration)
        return func(request, *args, **kwargs)
    return inner
