# coding=utf-8
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .navigation.views import HomeNavigationView, StaticNavigationView
from .content.views import NewsDetailView, NewsListView, InfoDetailView, GalleryListView, GalleryDetailView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeNavigationView.as_view(template_name='home.html'), name='home'),
    url(r'^calendar/$', StaticNavigationView.as_view(template_name='calendar.html', title=_("Calendar")), name='calendar'),
    url(r'^contacts/$', StaticNavigationView.as_view(template_name='contacts.html', title=_("Contacts")), name='contacts'),

    url(r'^news/$', NewsListView.as_view(), name='news_list'),
    url(r'^news/(?P<pk>[-\w]+)/$', NewsDetailView.as_view(), name='news_detail'),

    url(r'^info/(?P<slug>[-\w]+)/$', InfoDetailView.as_view(), name='info_detail'),
    url(r'^gallery/$', GalleryListView.as_view(), name='gallery_list'),
    url(r'^gallery/(?P<slug>[-\w]+)/$', GalleryDetailView.as_view(), name='gallery_detail'),

    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# Media serve ONLY for dev server, in production this should be done by server
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
    urlpatterns += patterns('',
        (r'^(?P<path>(favicon.ico|favicon.png|robots.txt))$',
            'django.views.static.serve',
            {'document_root': settings.WWW_ROOT}),
    )
