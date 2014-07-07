# coding=utf-8

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from feincms.admin.tree_editor import TreeEditor, ajax_editable_boolean
from feincms.admin.item_editor import ItemEditor
from modeltranslation.admin import TranslationAdmin
from .models import Region, PlaceType, Place, TrackPlaces, Track
from sorl.thumbnail.admin import AdminImageMixin


class RegionAdmin(AdminImageMixin, TranslationAdmin, ItemEditor):
    list_display = ('name', 'type', 'map_id', 'map_color')
    list_editable = ('map_id', 'map_color')

admin.site.register(Region, RegionAdmin)


class PlaceTypeAdmin(TreeEditor, TranslationAdmin):
    list_display = ('name', 'active_toggle', )
    active_toggle = ajax_editable_boolean('active', _("active"))
    prepopulated_fields = {'slug': ['name_en']}

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(PlaceTypeAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        self.patch_translation_field(db_field, field, **kwargs)
        return field

admin.site.register(PlaceType, PlaceTypeAdmin)


class PlaceAdmin(TreeEditor, TranslationAdmin):
    list_display = ('name', 'url', 'lon', 'lat', 'active_toggle', )
    active_toggle = ajax_editable_boolean('active', _("active"))
    list_filter = ('type', )
    list_per_page = 50
    list_select_related = True
    search_fields = ['name', 'slug', 'url', 'address', 'phone', 'url', 'desc']

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(PlaceAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        self.patch_translation_field(db_field, field, **kwargs)
        return field

admin.site.register(Place, PlaceAdmin)


class TrackPlacesInline(admin.TabularInline):
    model = TrackPlaces
    fields = 'type', 'order', 'place'
    raw_id_fields = 'place',


class TrackAdmin(AdminImageMixin, TranslationAdmin):
    list_display = ('name', 'slug', 'track')
    list_editable = ('slug', )
    filter_horizontal = 'places',
    prepopulated_fields = {'slug': ['name_en']}
    inlines = [TrackPlacesInline]

admin.site.register(Track, TrackAdmin)
