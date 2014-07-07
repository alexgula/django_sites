from copy import copy


def permalink(func):
    """
    Decorator that calls urlresolvers.reverse() to return a URL using
    parameters returned by the decorated function "func".

    "func" should be a function that returns a tuple in one of the
    following formats:
        (viewname, viewargs)
        (viewname, viewargs, viewkwargs)

    Changed importing of reverse() due to the localeurl issue.
    """
    from django.core import urlresolvers
    def inner(*args, **kwargs):
        bits = func(*args, **kwargs)
        return urlresolvers.reverse(bits[0], None, *bits[1:3])
    return inner


def redirect(request, to, *args, **kwargs):
    return redirect(request, to, *args, **kwargs)


def params_set_format(*args, **kwargs):
    return params_format(params_set(*args, **kwargs))


def params_set(param_dict, param_name, param_values):
    params = copy(param_dict)
    params.setlist(param_name, param_values)
    return params


def params_format(param_dict):
    params = param_dict.urlencode()
    if params:
        return u"?" + params
    else:
        return u""
