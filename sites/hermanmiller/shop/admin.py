# coding=utf-8
from django.contrib import admin
from .models import Customer, Order, OrderItem, PaymentLiqPay


class OrderInline(admin.TabularInline):
    model = Order


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = 'name', 'phone', 'email', 'code'
    inlines = [OrderInline]

admin.site.register(Customer, CustomerAdmin)


class OrderItemInline(admin.StackedInline):
    model = OrderItem


class PaymentLiqPayInline(admin.StackedInline):
    model = PaymentLiqPay


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = 'id', 'name', 'phone', 'email', 'status', 'sum_eur', 'sum_uah'
    inlines = [PaymentLiqPayInline, OrderItemInline]

admin.site.register(Order, OrderAdmin)
