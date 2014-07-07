#coding: utf-8
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
from tekhnoland.content.views import StaticContentView, HomeStaticContentView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeStaticContentView.as_view(code='home', title=u"Добро пожаловать!"), name='home'),
    url(r'^about/$', StaticContentView.as_view(code='about', title=u"О компании"), name='about'),
    url(r'^conditions/$', StaticContentView.as_view(code='conditions', title=u"Как заказать"), name='conditions'),
    url(r'^delivery/$', StaticContentView.as_view(code='delivery', title=u"Доставка"), name='delivery'),
    url(r'^contacts/$', StaticContentView.as_view(code='contacts', title=u"Контакты"), name='contacts'),

    url(r'^account/', include('tekhnoland.account.urls', 'account', 'account')),

    url(r'^news/', include('tekhnoland.news.urls', 'news', 'news')),

    url(r'^feedback/', include('tekhnoland.feedback.urls', 'feedback', 'feedback')),

    url(r'^catalog/', include('tekhnoland.catalog.urls', 'catalog', 'catalog')),

    url(r'^poll/', include('tekhnoland.polls.urls', 'polls', 'polls')),

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
