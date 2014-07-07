# coding=utf-8
from django.contrib import admin
from .models import Partner


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'important', 'url', )
    list_editable = ('important', 'url', )

admin.site.register(Partner, PartnerAdmin)
