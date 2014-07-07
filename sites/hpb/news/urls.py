__author__ = 'Irina Galchevska'
from django.conf.urls import *
from .views import one_news_list, one_news_details

urlpatterns = patterns('',
    url(r'^$', one_news_list, {}, 'one_news_list'),
    url(r'^(?P<news_id>[\d]+)/$',one_news_details, {}, 'news_details') # (... viewname, url-config(see models-get_absolute_url)
)
