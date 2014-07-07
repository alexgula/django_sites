# coding=utf-8
from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from .models import Page, Photo

class PhotoInline(AdminImageMixin, admin.StackedInline):
    model = Photo

class PageAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = 'title',
    inlines = [PhotoInline]

admin.site.register(Page, PageAdmin)
admin.site.register(Photo)
