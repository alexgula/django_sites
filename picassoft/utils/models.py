# coding=utf-8
from django.db import models
from django.http import Http404


def filter_choice(choices, key):
    """Find value by key in the list of choices of a model field."""
    choice = filter(lambda x: x[0] == key, choices)
    if len(choice) == 1:
        choice = choice[0]
    else:
        raise Http404()
    return choice[1]


class ActiveManager(models.Manager):
    def active(self):
        return self.get_query_set().filter(active=True)
