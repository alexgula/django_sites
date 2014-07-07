# coding=utf-8
from django.conf import settings
from django.utils import translation

def country(request):
    language_code = translation.get_language()
    country_code = settings.COUNTRY_CODE_CONVERSION.get(language_code, language_code)
    return {'COUNTRY_CODE': country_code}
