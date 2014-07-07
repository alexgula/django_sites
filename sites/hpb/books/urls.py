__author__ = 'Irina Galchevska'
from django.conf.urls import *
from .views import book_list, book_details

urlpatterns = patterns('',
    url(r'^$',book_list, {}, 'book_list'),
    url(r'^(?P<book_slug>[-\w]+)/(?P<page_num>[\d]+)/$',book_details, {}, 'book_details'), # (... viewname, url-config(see models-get_absolute_url)
)
