# coding=utf-8

from django.contrib import admin
from .models import PriceType, ProductStockUnit, Product, ProductStockUnitPrice, Order, OrderItem


class PriceTypeAdmin(admin.ModelAdmin):
    list_display = 'code', 'name', 'currency', 'currency_rate',

admin.site.register(PriceType, PriceTypeAdmin)


class ProductStockUnitInline(admin.TabularInline):
    model = ProductStockUnit
    raw_id_fields = 'product',


class ProductAdmin(admin.ModelAdmin):
    list_display = 'part_number', 'name',
    search_fields = 'part_number', 'name',
    raw_id_fields = 'replacements',
    inlines = [ProductStockUnitInline]

admin.site.register(Product, ProductAdmin)


class ProductStockUnitPriceInline(admin.TabularInline):
    model = ProductStockUnitPrice
    raw_id_fields = 'stock_unit',


class ProductStockUnitAdmin(admin.ModelAdmin):
    inlines = [ProductStockUnitPriceInline]
    search_fields = 'product__part_number', 'product__part_number_search', 'product__name',
    raw_id_fields = 'product',

admin.site.register(ProductStockUnit, ProductStockUnitAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = 'id', 'date', 'customer_full_name', 'status', 'payment_type',
    inlines = [OrderItemInline]
    raw_id_fields = 'customer',
    search_fields = 'id', 'code',

admin.site.register(Order, OrderAdmin)
