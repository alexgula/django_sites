# coding=utf-8
from functools import wraps, partial, update_wrapper
import inspect


def initializer(fun):
    """Init class members from (usually constructor) parameters.

    Example of usage:
    class process:
        @initializer
        def __init__(self, PID, PPID, cmd, FDs, reachable, user):
            pass

    >>> c = process(1, 2, 3, 4, 5, 6)
    >>> c.PID
    1
    >>> dir(c)
    ['FDs', 'PID', 'PPID', '__doc__', '__init__', '__module__', 'cmd', 'reachable', 'user'

    """
    names, varargs, keywords, defaults = inspect.getargspec(fun)
    @wraps(fun)
    def wrapper(self, *args, **kargs):
        for name, arg in zip(names[1:], args) + kargs.items():
            setattr(self, name, arg)
        fun(self, *args, **kargs)
    return wrapper


class memoized(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.

    cached_property (see later) is more tested but simpler.
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)
    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__
    def __get__(self, obj, objtype):
        """Support instance methods."""
        return partial(self.__call__, obj)


class cached_property(object):
    """cached_property(func) -> a descriptor
    This decorator implements an object's property which is computed
    the first time it is accessed, and which value is then stored in
    the object's __dict__ for later use. If the attribute is deleted,
    the value will be recomputed the next time it is accessed.

    Usage:
    User.profile = cached_property('profile', lambda self: CustomerProfile.objects.get_or_create(user=self)[0])
    """
    def __init__(self, name, func):
        update_wrapper(self, func)
        self.func = func
        self.name = name

    def __get__(self, obj, cls):
        if obj is None:
            return self

        try:
            cache = obj._property_cache
        except AttributeError:
            cache = {}
            obj._property_cache = cache

        try:
            return cache[self.name]
        except KeyError:
            value = self.func(obj)
            cache[self.name] = value
            return value
