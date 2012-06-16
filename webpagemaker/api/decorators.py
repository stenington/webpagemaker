from django.core.cache import cache
from django.http import HttpResponseBadRequest, HttpResponseForbidden
import hashlib

def throttle_view(func, methods=None, duration=15):
    """If I was a better programmer, I would get this to work with passed arguments,
    however - it's just not in the cards tonight. hence ...
    TODO: make this thing actually take arguments
    """
    def inner(request, *args, **kwargs):
        throttled_methods = methods if methods else ['POST', 'GET']
        if request.method in throttled_methods:
            remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or \
                          request.META.get('REMOTE_ADDR')
            key = (hashlib.md5('%s.%s' % (remote_addr, request.path_info))
                   .hexdigest())
            if cache.get(key):
                return HttpResponseForbidden("Sorry, you can only publish a page every %s seconds, try again in a bit" % duration)
            else:
                cache.set(key, True, duration)
                return func(request, *args, **kwargs)
    return inner
                    
