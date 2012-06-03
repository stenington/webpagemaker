from functools import wraps
from django.conf import settings
from django.utils.decorators import available_attrs

def development_cors(func):
    @wraps(func, available_attrs(func))
    def inner(*args, **kwargs):
        response = func(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    
    if settings.DEV:
        return inner
    
    return func

