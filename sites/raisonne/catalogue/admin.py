# coding=utf-8

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Category, Term, Author, ContemporaryType, AuthorContemporary, WorkLot, Work, Deal, LifePeriod, Owner
from ..auction.models import Bid
from django.utils.translation import ugettext_lazy as _

def resave(modeladmin, request, queryset):
    for model in queryset:
        model.save()
resave.short_description = u"Re-save to trigger actions"


def load_variants(modeladmin, request, queryset):
    for model in queryset:
        model.image_variants(overwrite=True)
load_variants.short_description = u"Load image variants"


class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'slug', 'weight', )
    #list_editable = ('slug', 'weight', )

admin.site.register(Category, CategoryAdmin)


class TermAdmin(TranslationAdmin):
    list_display = ('name', 'slug', 'abbr', 'weight', )
    #list_editable = ('slug', 'weight', )
    list_filter = ('category', )
    prepopulated_fields = {'slug': ['name_en']}

admin.site.register(Term, TermAdmin)


class AuthorAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ['name_en']}
    exclude = ('filter', )
    filter_horizontal = ('terms', )
    actions = [resave]
    list_display = ('pk', 'name', 'slug', 'date_birth', 'date_death', )
    list_display_links = ('pk', 'name', )
    #list_editable = ('date_birth', 'date_death', )

admin.site.register(Author, AuthorAdmin)


class ContemporaryTypeAdmin(TranslationAdmin):
    pass

admin.site.register(ContemporaryType, ContemporaryTypeAdmin)


class AuthorContemporaryAdmin(admin.ModelAdmin):
    pass

admin.site.register(AuthorContemporary, AuthorContemporaryAdmin)


class LifePeriodAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ['name_en']}
    list_display = ('name', 'slug', 'year_begin', 'year_end')
    list_filter = ('author', )
    #list_editable = ('slug', 'year_begin', 'year_end')

admin.site.register(LifePeriod, LifePeriodAdmin)


class WorkLotInline(admin.TabularInline):
    model = WorkLot


class WorkAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ['name_en']}
    exclude = ('filter', )
    filter_horizontal = ('terms', 'periods', )
    list_display = ('pk', 'name', 'slug', 'pub_date', 'author', 'years', 'height', 'width', 'image_offset_h', 'image_offset_v', 'is_listed', )
    list_display_links = ('pk', 'name', )
    list_editable = ('years', 'height', 'width', 'image_offset_h', 'image_offset_v', 'is_listed', ) # Crashes admin o.O
    list_filter = ('author', 'terms', 'periods', )
    search_fields = ['id', 'slug', 'name_uk', 'name_ru', 'name_en', 'name_fr']
    readonly_fields = ('rating_value', )
    actions = [resave, load_variants]
    save_on_top = True
    inlines = [
        WorkLotInline,
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(WorkAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ('years', 'height', 'width', ):
            field.widget.attrs['style'] = 'width: 8em; ' + field.widget.attrs.get('style', '')
        return field

admin.site.register(Work, WorkAdmin)


class OwnerAdmin(TranslationAdmin):
    pass

admin.site.register(Owner, OwnerAdmin)


class DealAdmin(TranslationAdmin):
    pass

admin.site.register(Deal, DealAdmin)


class BidInline(admin.TabularInline):
    model = Bid


class WorkLotAdmin(admin.ModelAdmin):
    list_display = ('pk', '__unicode__', 'is_open', 'can_bid', 'start_date', 'close_date', 'start_price', 'last_price', 'bid_count', 'buyout_price', 'buyout_cancel_price', 'estimate_price_start', 'estimate_price_end', )
    list_display_links = ('pk', '__unicode__')
    #list_editable = ('is_open', 'start_date', 'close_date', 'start_price', 'buyout_price', 'buyout_cancel_price', 'estimate_price_start', 'estimate_price_end', )
    fieldsets = (
        (None, {
            'fields': ('work', 'is_open', 'can_bid', ),
        }),
        (_("Dates"), {
            'fields': ('start_date', 'close_date', ),
        }),
        (_("Prices"), {
            'fields': ('start_price', 'buyout_price', 'buyout_cancel_price', 'estimate_price_start', 'estimate_price_end', ),
        }),
    )
    raw_id_fields = ('work', )
    inlines = [
        BidInline,
    ]

admin.site.register(WorkLot, WorkLotAdmin)
