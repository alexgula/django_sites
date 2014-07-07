# coding=utf-8

from django.contrib import admin
from .models import Currency

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('lang', 'name', 'code', 'rate', )
    list_editable = ('name', 'code', 'rate', )

admin.site.register(Currency, CurrencyAdmin)
