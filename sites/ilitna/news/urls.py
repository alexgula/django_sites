from django.conf.urls import patterns, url
from .views import NewsListView, NewsDetailView

urlpatterns = patterns('',
    url(r'^$', NewsListView.as_view(), name='list'),
    url(r'^(?P<pk>[\d]+)/$', NewsDetailView.as_view(), name='detail'),
)
