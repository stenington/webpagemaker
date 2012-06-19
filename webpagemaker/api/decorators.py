import functools
import hashlib

from django.core.cache import cache
from django.http import HttpResponseForbidden


def throttle_view(methods=None, duration=15):
    """Decorator that throttles the specified methods ``POST`` and ``GET``
    by default, uses ``X_FORWARDED_FOR`` or ``HTTP_X_FORWARDED_FOR`` or ``REMOTE_ADDR`` to determine
    the origin of the request.

    Usage:

    - Throttle with the ``POST`` method by 30 seconds

    @throttle_view(methods=['POST'], duration=30)

    - Throttle with the default values

    @throttle_view()
    """
    def decorator(function):
        @functools.wraps(function)
        def inner(request, *args, **kwargs):
            throttled_methods = methods if methods else ['POST', 'GET']
            if request.method in throttled_methods:
                remote_addr = request.META.get('X_FORWARDED_FOR') or request.META.get('HTTP_X_FORWARDED_FOR') or \
                    request.META.get('REMOTE_ADDR')
                key = (hashlib.md5('%s.%s' % (remote_addr, request.path_info))
                       .hexdigest())
                if cache.get(key):
                    return HttpResponseForbidden("Sorry, you can only publish a page every %s seconds, try again in a bit" % duration)
                else:
                    cache.set(key, True, duration)
            return function(request, *args, **kwargs)
        return inner
    return decorator
