# coding=utf-8
from django.contrib import admin
from .models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = ('action_date', 'success', 'results', )
    search_fields = ('results', )
    date_hierarchy = 'action_date'
    list_filter = ('success', )

admin.site.register(Log, LogAdmin)
