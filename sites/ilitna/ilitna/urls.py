from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings

from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += i18n_patterns(
    '',

    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    (r'news/', include('news.urls', 'news', 'news')),
    (r'library/', include('library.urls', 'library', 'library')),

    (r'^rosetta/', include('rosetta.urls')),

    (r'', include('page.urls', 'page', 'page')),
)

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
