# coding=utf-8
__author__ = 'Irina Galchevska'

from django.conf.urls import *
from .views import fondtask_list

urlpatterns = patterns('',
    url(r'^$', fondtask_list, {}, 'fond_tasks'),
)
