from django.contrib import admin
from django.db.models.expressions import F
from sorl.thumbnail.admin import AdminImageMixin
from .models import Book, Part

def plus_one(modeladmin, request, queryset):
    for part in queryset.order_by('-order'):
        in_book_part = part.in_book
        part_order = part.order
        Part.objects\
            .filter(in_book=in_book_part).filter(order__gte=part_order)\
            .update(order=F('order') + 1)
plus_one.short_description = "below: order=order+1"

def minus_one(modeladmin, request, queryset):
    for part in queryset.order_by('-order'):
        in_book_part = part.in_book
        part_order = part.order
        Part.objects\
            .filter(in_book=in_book_part).filter(order__gte=part_order)\
            .update(order=F('order') - 1)
minus_one.short_description = "choose one below: order=order-1"


class BookAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = 'author', 'title'
    prepopulated_fields = {'slug': ('title',)}


class PartAdmin(admin.ModelAdmin):
    list_display = 'in_book', 'title', 'page_num', 'level', 'order'
    list_editable =  'page_num', 'level', 'order'
    list_filter =  'in_book',
    exclude = 'text_html',
    prepopulated_fields = {'slug': ('title',)}
    actions = [plus_one, minus_one]

admin.site.register(Book,BookAdmin)
admin.site.register(Part,PartAdmin)
