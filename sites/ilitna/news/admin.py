# coding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from feincms.admin.item_editor import ItemEditor
from feincms.admin.tree_editor import ajax_editable_boolean
from modeltranslation.admin import TranslationAdmin
from .models import News
from sorl.thumbnail.admin import AdminImageMixin


class NewsAdmin(AdminImageMixin, TranslationAdmin):
    list_display = 'title', 'pub_date', 'active_toggle',
    search_fields = 'title', 'text'
    date_hierarchy = 'pub_date'
    list_filter = 'pub_date',
    active_toggle = ajax_editable_boolean('active', _("Active"))

admin.site.register(News, NewsAdmin)
