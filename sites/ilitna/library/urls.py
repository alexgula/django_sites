from django.conf.urls import patterns, url
from .views import AuthorListView, AuthorDetailView, WorkListView, WorkDetailView,\
    PublisherListView, PublisherDetailView, PublicationListView, PublicationDetailView

urlpatterns = patterns('',
    url(r'^authors/$', AuthorListView.as_view(), name='author_list'),
    url(r'^authors/(?P<slug>[-\w]+)/$', AuthorDetailView.as_view(), name='author_detail'),

    url(r'^works/$', WorkListView.as_view(), name='work_list'),
    url(r'^works/(?P<slug>[-\w/]+)/$', WorkDetailView.as_view(), name='work_detail'),

    url(r'^publishers/$', PublisherListView.as_view(), name='publisher_list'),
    url(r'^publishers/(?P<slug>[-\w]+)/$', PublisherDetailView.as_view(), name='publisher_detail'),

    url(r'^publications/$', PublicationListView.as_view(), name='publication_list'),
    url(r'^publications/(?P<isbn>[\d]+)/$', PublicationDetailView.as_view(), name='work_detail'),
)
