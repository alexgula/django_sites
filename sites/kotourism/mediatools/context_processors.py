# coding=utf-8
from django.conf import settings

def thumbnail_settings(request):
    return {'THUMBNAIL_SETTINGS': settings.THUMBNAIL_SETTINGS}
