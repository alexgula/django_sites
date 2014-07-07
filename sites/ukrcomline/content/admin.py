# coding=utf-8
from django.contrib import admin
from feincms.admin.item_editor import ItemEditor
from .models import News, Portfolio, Certificate, StaticPage
from sorl.thumbnail.admin import AdminImageMixin


class NewsAdmin(AdminImageMixin, ItemEditor):
    list_display = 'title', 'created_on',
    list_display_links = 'title',
    search_fields = 'title', 'desc',

admin.site.register(News, NewsAdmin)


class PortfolioAdmin(AdminImageMixin, ItemEditor):
    list_display = 'title', 'created_on',
    list_display_links = 'title',
    search_fields = 'title', 'desc',

admin.site.register(Portfolio, PortfolioAdmin)


class CertificateAdmin(AdminImageMixin, ItemEditor):
    list_display = 'id', 'title', 'created_on',
    list_display_links = 'title',
    search_fields = 'title', 'desc',

admin.site.register(Certificate, CertificateAdmin)


class StaticPageAdmin(AdminImageMixin, ItemEditor):
    list_display = 'id', 'title', 'created_on',
    list_display_links = 'title',
    search_fields = 'title', 'desc',

admin.site.register(StaticPage, StaticPageAdmin)
