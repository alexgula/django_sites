# coding=utf-8

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Registration, CustomerProfile


class RegistrationAdmin(admin.ModelAdmin):
    list_display = 'username', 'last_name', 'first_name', 'father_name', 'email', 'post_date', 'username1c',
    search_fields = 'username', 'last_name', 'first_name', 'father_name', 'username1c',
    date_hierarchy = 'post_date'
    actions = ['activate_users', 'resend_activation_email']

    def activate_users(self, request, queryset):
        for registration in queryset:
            Registration.objects.activate(registration.activation_key)
    activate_users.short_description = u"Активировать пользователей"

    def resend_activation_email(self, request, queryset):
        for registration in queryset:
            if not registration.activation_key_expired():
                registration.send_activation_email()
    resend_activation_email.short_description = "Повторно выслать сообщение для активации"

admin.site.register(Registration, RegistrationAdmin)


admin.site.unregister(User)

class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile

class CustomerProfileAdmin(UserAdmin):
    inlines = [CustomerProfileInline]

admin.site.register(User, CustomerProfileAdmin)
