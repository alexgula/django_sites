# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
from django.conf.urls import *
from .static_content.views import content

admin.autodiscover()

urlpatterns = patterns('',
    (r'^events/', include('hpb.events.urls')),
    (r'^family/', include('hpb.family.urls')),
    (r'^news/', include('hpb.news.urls')),
    (r'^museum/', include('hpb.fondtasks.urls')),
    (r'^scicenter/', include('hpb.scicenter.urls')),
    (r'^books/', include('hpb.books.urls')),

    #static blocks
    (r'^$', content, {'template_name': 'main_page'},'home'),

    (r'^timetable/', content, {'template_name': 'timetable'},'time_table'),

    (r'^contacts/', content, {'template_name': 'contacts'},'contact'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^rosetta/', include('rosetta.urls')),
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
