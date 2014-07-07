# coding=utf-8
from functools import wraps
from django.core.cache import cache


def cached(key):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            value = cache.get(key)
            if value is None:
                value = f(*args, **kwargs)
                cache.set(key, value)
            return value
        return wrapper
    return decorator
