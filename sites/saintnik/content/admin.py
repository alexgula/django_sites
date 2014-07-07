# coding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from feincms.admin.editor import ajax_editable_boolean
from feincms.admin.item_editor import ItemEditor
from feincms.admin.tree_editor import TreeEditor
from modeltranslation.admin import TranslationAdmin
from .models import News, InfoPage, GalleryPage
from sorl.thumbnail.admin import AdminImageMixin


class NewsAdmin(AdminImageMixin, TranslationAdmin, ItemEditor):
    list_display = 'title', 'pub_date', 'active_toggle',
    search_fields = 'title', 'text'
    date_hierarchy = 'pub_date'
    list_filter = 'pub_date',
    active_toggle = ajax_editable_boolean('active', _('active'))

admin.site.register(News, NewsAdmin)


class InfoPageAdmin(AdminImageMixin, TranslationAdmin, ItemEditor, TreeEditor):
    list_display = 'title', 'slug', 'active_toggle',
    search_fields = 'slug', 'title', 'text'
    active_toggle = ajax_editable_boolean('active', _('active'))

admin.site.register(InfoPage, InfoPageAdmin)


class GalleryPageAdmin(AdminImageMixin, TranslationAdmin, ItemEditor, TreeEditor):
    list_display = 'title', 'slug', 'active_toggle',
    search_fields = 'slug', 'title', 'text'
    active_toggle = ajax_editable_boolean('active', _('active'))

admin.site.register(GalleryPage, GalleryPageAdmin)
