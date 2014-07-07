# coding=utf-8
import os
from django.contrib import admin
from django.conf import settings
from .models import Site, Search, Results
from picassoft.search_engines import GoogleEngine, YandexEngine, YandexXMLEngine

LOG_DIR = os.path.join(settings.SITE_ROOT, 'tmp')

ENGINES = [
    {'name': u'Google UA', 'engine': GoogleEngine(debug=settings.DEBUG, log_dir=LOG_DIR, address='http://google.com.ua/')},
    #{'name': u'Yandex UA', 'engine': YandexEngine, 'address': 'http://yandex.ua/'},
    {'name': u'Yandex XML', 'engine': YandexXMLEngine(u'seo-lyamin', u'03.133090775:96d22c1d0123309d56f57ecccbf7c06e')},
]

def seach_keyword(search, site, keyword):
    for engine_conf in ENGINES:
        engine = engine_conf['engine']
        position, result = engine.search(keyword, site.site_domain)
        url = result.url if result else None
        Results.objects.create(site=site, search=search, keyword=keyword, engine=engine_conf['name'], position=position,
                               url=url)

def get_positions_admin_option(modeladmin, request, queryset):
    search = Search.objects.create()
    for site in queryset:
        keywords = site.keywords.splitlines()
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword and keyword[0] != u'#':
                seach_keyword(search, site, keyword)

get_positions_admin_option.short_description = u"Узнать позиции"


class SiteAdmin(admin.ModelAdmin):
    list_display = 'site_domain',
    search_fields = 'site_domain',
    actions = [get_positions_admin_option]

admin.site.register(Site, SiteAdmin)


class ResultInline(admin.TabularInline):
    model = Results


class SearchAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    inlines = [ResultInline]

admin.site.register(Search, SearchAdmin)


class ResultAdmin(admin.ModelAdmin):
    list_display = 'site', 'keyword', 'search', 'engine', 'position',
    list_filter = 'site', 'search', 'engine'

admin.site.register(Results, ResultAdmin)
