# coding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import News, StaticPage
from sorl.thumbnail.admin import AdminImageMixin
from feincms.admin.tree_editor import ajax_editable_boolean
from feincms.admin.item_editor import ItemEditor


class NewsAdmin(ItemEditor, AdminImageMixin):
    list_display = 'title', 'created_on',
    list_display_links = 'title',
    search_fields = 'title', 'desc',
    active_toggle = ajax_editable_boolean('active', _('active'))

admin.site.register(News, NewsAdmin)


class StaticPageAdmin(ItemEditor, AdminImageMixin):
    list_display = 'title', 'slug',
    list_display_links = 'title',
    search_fields = 'title', 'desc',
    active_toggle = ajax_editable_boolean('active', _('active'))

admin.site.register(StaticPage, StaticPageAdmin)
