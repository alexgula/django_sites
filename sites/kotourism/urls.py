from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin
from django.contrib.auth.views import login

from .events.views import ServiceEventListByMonth, TypedEventList, EventListByYear, EventListByMonth, EventListByDate, EventDetail
from .events.feeds import EventFeed
from .places.views import PlaceList, PlaceDetail, RegionList, RegionDetail, ServiceRegionMap, ServiceTourMap, TrackList, TrackDetail
from .navigation.views import TemplateNavigationView, StaticNode
from .interop.views import ImportXML
from .search.views import SearchView
from .exhibit.views import ExhibitDetail
from .partners.views import PartnerList
from .photocontest.views import PhotoContestList, PhotoContestVote, PhotoContestRegister,\
    PhotoContestLogin, PhotoContestLogout, PhotoContestRegisterConfirm, PhotoContestUpload, PhotoContestTerms

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    # Static pages
    url(r'^contacts/$', TemplateNavigationView.as_view(template_name='contacts.html', trail=[StaticNode(_("Contacts"), 'contacts')]), name='contacts'),
    url(r'^adminmap/$', TemplateNavigationView.as_view(template_name='adminmap.html', trail=[StaticNode(_("Administrative Map"), 'adminmap')]), name='adminmap'),
    url(r'^tourmap/$', TemplateNavigationView.as_view(template_name='tourmap.html', trail=[StaticNode(_("Tourists Map"), 'tourmap')]), name='tourmap'),
    url(r'^audioguide/$', TemplateNavigationView.as_view(template_name='audioguide.html', trail=[StaticNode(_("Audio Guide"), 'audioguide')]), name='audioguide'),
    url(r'^film/$', TemplateNavigationView.as_view(template_name='film.html', trail=[StaticNode(_("Film"), 'film')]), name='film'),
    url(r'^tourguide/$', TemplateNavigationView.as_view(template_name='tourguide.html', trail=[StaticNode(_("Tourists Guide"), 'tourguide')]), name='tourguide'),
    url(r'^video/$', TemplateNavigationView.as_view(template_name='video.html', trail=[StaticNode(_("Video"), 'video')]), name='video'),

    # Events
    url(r'^events/(?P<type_slug>[-\w]+)/$', TypedEventList.as_view(), name='typed_event_list'),
    url(r'^events/(?P<type_slug>[-\w]+)/(?P<year>\d{4})/$', EventListByYear.as_view(), name='event_list_by_year'),
    url(r'^events/(?P<type_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/$', EventListByMonth.as_view(), name='event_list_by_month'),
    url(r'^events/(?P<type_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', EventListByDate.as_view(), name='event_list_by_date'),
    url(r'^events/(?P<type_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', EventDetail.as_view(), name='event_detail'),

    # Places
    url(r'^places/(?P<type_slug>[-\w]+)/$', PlaceList.as_view(), name='place_list'),
    url(r'^places/(?P<type_slug>[-\w]+)/(?P<slug>[-\w]+)/$', PlaceDetail.as_view(), name='place_detail'),

    # Tracks
    url(r'^tracks/$', TrackList.as_view(), name='track_list'),
    url(r'^tracks/(?P<slug>[-\w]+)/$', TrackDetail.as_view(), name='track_detail'),

    # Regions
    url(r'^regions/$', RegionList.as_view(), name='region_list_all'),
    url(r'^regions/(?P<type_slug>[-\w]+)/$', RegionList.as_view(), name='region_list'),
    url(r'^regions/(?P<type_slug>[-\w]+)/(?P<slug>[-\w]+)/$', RegionDetail.as_view(), name='region_detail'),

    # Exhibits
    url(r'^exhibit/(?P<slug>[-\w]+)/$', ExhibitDetail.as_view(), name='exhibit_detail'),

    # Partners
    url(r'^partners/$', PartnerList.as_view(), name='partner_list'),

    # Photo Contest
    url(r'^photo-contest/$', PhotoContestList.as_view(), name='photocontest_list'),
    url(r'^photo-contest/vote/$', PhotoContestVote.as_view(), name='photocontest_vote'),
    url(r'^photo-contest/register/$', PhotoContestRegister.as_view(), name='photocontest_register'),
    url(r'^photo-contest/register/(?P<activation_key>.+)/$', PhotoContestRegisterConfirm.as_view(), {}, name='photocontest_register_confirm'),
    url(r'^photo-contest/upload/$', PhotoContestUpload.as_view(), name='photocontest_upload'),
    url(r'^photo-contest/login/$', PhotoContestLogin.as_view(),  name='photocontest_login'),
    url(r'^photo-contest/logout/$', PhotoContestLogout.as_view(),  name='photocontest_logout'),
    url(r'^photo-contest/terms/$', PhotoContestTerms.as_view(),  name='photocontest_terms'),

    # AJAX Services
    url(r'^service/events/(?P<year>[\d]+)/(?P<month>[\d]+)/$', ServiceEventListByMonth.as_view(), name='news_monthly'),
    url(r'^service/places/region-map/$', ServiceRegionMap.as_view(), name='region_map'),
    url(r'^service/places/tourmap/$', ServiceTourMap.as_view(), name='service_tourmap'),

    # Interop
    url(r'^interop/upload/$', ImportXML.as_view(), name='interop_import'),

    # Search
    url(r'^search/', SearchView.as_view(), name='search'),

    # RSS feeds
    url(r'^feed/events/(?P<type_slug>[-\w]+)/$', EventFeed(), name='feed_events'),

    # Rosetta
    url(r'^rosetta/', include('rosetta.urls')),

    # Admin
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
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
