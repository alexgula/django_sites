__author__ = 'Irina Galchevska'
from django.conf.urls import *
from .views import family_member_list, family_member_details, epbpage

urlpatterns = patterns('',
    url(r'^$',family_member_list, {}, 'family_member_list'),
    url(r'^(?P<member_id>[\d]+)/$',family_member_details, {}, 'family_member_details'), # (... viewname, url-config(see models-get_absolute_url)
    url(r'^hpb$',epbpage, {}, 'epbpage') # (... viewname, url-config(see models-get_absolute_url)
)

