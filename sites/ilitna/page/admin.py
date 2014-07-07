# coding=utf-8
from django.contrib import admin
from feincms.admin.item_editor import ItemEditor
from feincms.admin.tree_editor import TreeEditor
from modeltranslation.admin import TranslationAdmin
from .models import Page
from sorl.thumbnail.admin import AdminImageMixin


class PageAdmin(AdminImageMixin, TranslationAdmin, ItemEditor, TreeEditor):
    list_display = 'title', 'slug',
    search_fields = 'slug', 'title',

admin.site.register(Page, PageAdmin)
