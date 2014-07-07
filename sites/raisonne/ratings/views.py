# coding=utf-8

from django.http import HttpResponse
from functools import wraps

def rabid_rating(fun):
    @wraps(fun)
    def rabid_wrapper(*args, **kwargs):
        rating = fun(*args, **kwargs)
        return_value = "%s/%s stars ( %s votes)" % ( rating.stars, rating.max_stars, rating.total)
        return HttpResponse(return_value)
    return rabid_wrapper
