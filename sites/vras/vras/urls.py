# coding=utf-8
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from common.views import HomeNavigationView
from content.views import NewsListView, NewsDetailView, StaticPageView
from catalog.views import CategoryDetailView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += i18n_patterns('',
    url(r'^$', HomeNavigationView.as_view(), name='home'),

    url(r'^news/$', NewsListView.as_view(), name='news_list'),
    url(r'^news/(?P<pk>[\d]+)/$', NewsDetailView.as_view(), name='news_detail'),

    url(r'^products/(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name='category_detail'),

    url(r'^contacts/', include('feedback.urls', 'feedback', 'feedback')),

    url(r'^(?P<slug>[-\w]+)/$', StaticPageView.as_view(), name='static_page'),
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
