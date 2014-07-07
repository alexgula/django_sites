# coding=utf-8
from functools import wraps


def extract_context(*property_names):
    def wrapped(f):
        @wraps(f)
        def wrapper(context, *args, **kwargs):
            result = f(context, *args, **kwargs)
            for property_name in property_names:
                result[property_name] = context[property_name]
            return result
        return wrapper
    return wrapped
