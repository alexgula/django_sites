# coding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import News, NewsImage, StaticPage, StaticPageImage
from sorl.thumbnail.admin import AdminImageMixin
from feincms.admin.tree_editor import ajax_editable_boolean


class NewsImageInline(admin.TabularInline):
    model = NewsImage


class NewsAdmin(admin.ModelAdmin, AdminImageMixin):
    list_display = 'title', 'created_on',
    list_display_links = 'title',
    search_fields = 'title', 'desc',
    active_toggle = ajax_editable_boolean('active', _('active'))
    inlines = [NewsImageInline, ]

admin.site.register(News, NewsAdmin)


class StaticPageImageInline(admin.TabularInline):
    model = StaticPageImage


class StaticPageAdmin(admin.ModelAdmin, AdminImageMixin):
    list_display = 'title', 'slug',
    list_display_links = 'title',
    search_fields = 'title', 'desc',
    active_toggle = ajax_editable_boolean('active', _('active'))
    inlines = [StaticPageImageInline, ]

admin.site.register(StaticPage, StaticPageAdmin)
