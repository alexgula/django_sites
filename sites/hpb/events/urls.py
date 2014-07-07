__author__ = 'Irina Galchevska'
from django.conf.urls import *
from .views import event_list, event_details

urlpatterns = patterns('',
    url(r'^$',event_list, {}, 'event_list'),
    url(r'^(?P<event_id>[\d]+)/$',event_details, {}, 'event_details') # (... viewname, url-config(see models-get_absolute_url)
)
