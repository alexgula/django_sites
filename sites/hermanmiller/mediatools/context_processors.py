# coding=utf-8
import django.conf


def settings(request):
    return {'settings': django.conf.settings}
