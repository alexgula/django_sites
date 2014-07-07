# coding=utf-8
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import TextBlock


class TextBlockAdmin(TranslationAdmin, admin.ModelAdmin):
    list_display = 'code', 'comment', 'text',
    list_display_links = 'text',
    search_fields = 'text',

    def get_form(self, request, obj=None, **kwargs):
        self.readonly_fields = []
        if not request.user.is_superuser:
            self.readonly_fields.extend(['code', 'comment'])
        return super(TextBlockAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(TextBlock, TextBlockAdmin)
