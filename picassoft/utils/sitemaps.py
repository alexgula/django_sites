from django.conf import settings
from django.contrib.sitemaps import Sitemap
from localeurl.templatetags.localeurl_tags import chlocale


def _for_every_lang_code(objects):
    return [(object, lang[0]) for object in objects for lang in settings.LANGUAGES]


class MultiLocaleSitemap(Sitemap ):
    changefreq = "weekly"

    def items(self):
        return _for_every_lang_code(self._items())

    def location(self, obj):
        object, lang = obj
        return chlocale(object.get_absolute_url(), lang)
