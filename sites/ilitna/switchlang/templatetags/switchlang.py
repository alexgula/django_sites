# coding=utf-8
from django import template
from django.conf import settings
from django.utils import translation
from django.core.urlresolvers import resolve, reverse, Resolver404

register = template.Library()


def change_language(url, language_code):
    try:
        resolver = resolve(url)
    except Resolver404:
        # Probably we inside 404.html
        return None
    with translation.override(language_code):
        return reverse(resolver.view_name, args=resolver.args, kwargs=resolver.kwargs)


def prepare_lang(request, language_code):
    lang = translation.get_language_info(language_code)
    path = request.get_full_path()
    url = change_language(path, language_code)
    current = url == path
    return lang, url, current


@register.inclusion_tag('switchlang/switchlang.html', takes_context=True)
def language_switcher(context):
    languages = [prepare_lang(context['request'], lang[0]) for lang in settings.LANGUAGES]
    return dict(languages=languages, languages_count=len(languages))
