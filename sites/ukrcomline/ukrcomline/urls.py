# coding=utf-8
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from constance import config
from common.views import HomeNavigationView
from content.views import NewsListView, NewsDetailView,\
    PortfolioListView, PortfolioDetailView,\
    CertificateListView,\
    StaticPageView
from catalog.views import CategoryListView, CategoryDetailView
from interop.views import ImportXML
from search.views import SearchView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeNavigationView.as_view(), name='home'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^news/$', NewsListView.as_view(), name='news_list'),
    url(r'^news/(?P<pk>[\d]+)/$', NewsDetailView.as_view(), name='news_detail'),

    url(r'^install/$', PortfolioListView.as_view(), name='portfolio_list'),
    url(r'^install/(?P<pk>[\d]+)/$', PortfolioDetailView.as_view(), name='portfolio_detail'),

    url(r'^certificate/$', CertificateListView.as_view(), name='certificate_list'),

    url(r'^prod/$', CategoryListView.as_view(), name='category_list'),
    url(r'^prod/(?P<pk>[\d]+)/$', CategoryDetailView.as_view(), name='category_detail'),

    url(r'^interop/upload/$', ImportXML.as_view(), name='interop_upload'),

    url(r'^search/', SearchView.as_view(), name='search'),

    url(r'^{}/'.format(config.FEEDBACK_PAGE_SLUG), include('feedback.urls', 'feedback', 'feedback')),

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
