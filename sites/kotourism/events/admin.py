# coding=utf-8

from django.contrib import admin
from feincms.admin.item_editor import ItemEditor
from modeltranslation.admin import TranslationAdmin
from .models import Event
from sorl.thumbnail.admin import AdminImageMixin


class EventAdmin(AdminImageMixin, TranslationAdmin, ItemEditor):
    list_display = ('name', 'date_active_from', 'date_from', 'date_to', 'type', )
    prepopulated_fields = {'slug': ['name_en']}
    search_fields = ('name', 'desc', )
    date_hierarchy = 'date_from'
    list_filter = ('type', 'date_active_from', 'date_from', 'date_to', 'active', )
    raw_id_fields = ('place_link',)

admin.site.register(Event, EventAdmin)
