# coding=utf-8

from django.contrib import admin
from .models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = 'text', 'post_date',
    search_fields = 'text',
    date_hierarchy = 'post_date'

admin.site.register(News, NewsAdmin)
