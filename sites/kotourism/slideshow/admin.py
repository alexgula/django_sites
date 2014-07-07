# coding=utf-8

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Slide

class SlideAdmin(TranslationAdmin):
    list_display = ('slug', 'name', 'map_lon', 'map_lat', )
    list_editable = ('name', 'map_lon', 'map_lat', )
    prepopulated_fields = {'slug': ['name_en']}

admin.site.register(Slide, SlideAdmin)
