from django.conf.urls import patterns, url
from .views import PageDetailView

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', PageDetailView.as_view(), name='page'),
)
