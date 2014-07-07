from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('views',
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     url(r'', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
