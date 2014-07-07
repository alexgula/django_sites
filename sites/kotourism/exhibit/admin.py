# coding=utf-8
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline, TranslationStackedInline
from .models import Exhibit, ExhibitSection, ExhibitPartner, ExhibitMap
from sorl.thumbnail.admin import AdminImageMixin


class ExhibitSectionAdmin(AdminImageMixin, TranslationStackedInline):
    model = ExhibitSection


class ExhibitMapAdmin(TranslationTabularInline):
    model = ExhibitMap


class ExhibitPartnerAdmin(AdminImageMixin, TranslationTabularInline):
    model = ExhibitPartner


class ExhibitAdmin(AdminImageMixin, TranslationAdmin):
    list_display = 'slug', 'name',
    inlines = ExhibitPartnerAdmin, ExhibitSectionAdmin, ExhibitMapAdmin
    save_on_top = True

admin.site.register(Exhibit, ExhibitAdmin)
