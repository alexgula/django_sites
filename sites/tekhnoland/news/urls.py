from django.conf.urls import *

from .views import NewsList

urlpatterns = patterns('',
    # News list
    (r'^$',
        NewsList.as_view(), {}, 'list'),
)
