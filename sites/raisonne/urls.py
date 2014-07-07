# coding=utf-8
from django.conf.urls import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

urlpatterns = patterns('',
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^{}/'.format(settings.DAJAXICE_MEDIA_PREFIX), include('dajaxice.urls')),

    (r'^comments/', include('django.contrib.comments.urls')),

    (r'^rosetta/', include('rosetta.urls')),

    (r'', include('raisonne.catalogue.urls')),
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
