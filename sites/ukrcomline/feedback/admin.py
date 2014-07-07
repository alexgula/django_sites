# coding=utf-8
from django.contrib import admin
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = 'topic', 'name', 'phone', 'email', 'post_date',
    search_fields = 'topic', 'name', 'phone', 'city', 'email', 'text',
    date_hierarchy = 'post_date'

admin.site.register(Feedback, FeedbackAdmin)
