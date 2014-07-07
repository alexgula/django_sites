# coding=utf-8
from django.conf.urls import *
from .views import page_list

urlpatterns = patterns('',
    url(r'^$', page_list, {}, 'scicenter_page_list'),
)
