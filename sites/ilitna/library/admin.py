# coding=utf-8
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from feincms.admin.item_editor import ItemEditor
from feincms.admin.tree_editor import TreeEditor, ajax_editable_boolean
from modeltranslation.admin import TranslationAdmin
from .models import Author, Work, Publisher, Publication
from sorl.thumbnail.admin import AdminImageMixin


class AuthorAdmin(AdminImageMixin, TranslationAdmin):
    list_display = 'slug', 'first_name', 'family_name', 'active_toggle',
    search_fields = 'slug', 'first_name', 'family_name',
    active_toggle = ajax_editable_boolean('active', _("Active"))

admin.site.register(Author, AuthorAdmin)


class WorkAdmin(ItemEditor, TreeEditor):
    list_display = 'slug', 'title', 'active_toggle', 'listed_toggle',
    list_filter = 'authors__family_name',
    prepopulated_fields = {'slug': ('title', ), }
    search_fields = 'slug', 'authors__family_name', 'title', 'teaser',
    active_toggle = ajax_editable_boolean('active', _("Active"))
    listed_toggle = ajax_editable_boolean('listed', _("Show in List"))
    exclude = 'slug_trail',

admin.site.register(Work, WorkAdmin)


class PublisherAdmin(TranslationAdmin):
    list_display = 'slug', 'name',
    search_fields = 'slug', 'name',

admin.site.register(Publisher, PublisherAdmin)


class PublicationAdmin(admin.ModelAdmin):
    list_display = 'isbn', 'work', 'publisher', 'year', 'active_toggle',
    search_fields = 'work__title', 'publisher__name',
    active_toggle = ajax_editable_boolean('active', _("Active"))

admin.site.register(Publication, PublicationAdmin)
