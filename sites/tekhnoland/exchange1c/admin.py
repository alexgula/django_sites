# coding=utf-8
from django.contrib import admin
from .models import Exchange


class ExchangeAdmin(admin.ModelAdmin):
    list_display = 'code', 'exchange_type', 'date_start', 'status'
    date_hierarchy = 'date_start'
    list_filter = 'exchange_type', 'status'

admin.site.register(Exchange, ExchangeAdmin)
