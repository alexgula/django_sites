from django.conf.urls import *

from .views import home, content, work_list, work_search, author_detail, work_detail, work_vote, redirect_to_search, lot_list, lot_detail, service_make_bid
from .sitemaps import AuthorSitemap, WorkSitemap

sitemaps = {
    'authors': AuthorSitemap,
    'works': WorkSitemap,
}

urlpatterns = patterns('',
    # Sitemap
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    # Catalogue
    (r'^works/$', # Can be indexed
        work_list, {}, 'catalogue_list'),
    (r'^works/search/$', # Shouldn't be indexed
        work_search, {}, 'catalogue_search'),

    # Static includes
    (r'^about/$',
        content, {'template_name': 'about'}, 'content_about'),
    (r'^video/$',
        content, {'template_name': 'video'}, 'content_video'),
    (r'^contacts/$',
        content, {'template_name': 'contacts'}, 'content_contacts'),
    (r'^partners/$',
        content, {'template_name': 'partners'}, 'content_partners'),

    (r'^auction/$',
        lot_list, {}, 'catalogue_lot_list'),
    (r'^auction/lot/(?P<author_slug>[-\w]+)/(?P<work_slug>[-\w]+)/$',
        lot_detail, {}, 'catalogue_lot_detail'),

    # Redirects from old URLs for bots
    (r'^authors/works/$',
        redirect_to_search, {}),
    (r'^unknown/works/$',
        redirect_to_search, {}),
    (r'^(?P<author_slug>[-\w]+)/search/$',
        redirect_to_search, {}),

    (r'^(?P<author_slug>[-\w]+)/$',
        author_detail, {}, 'catalogue_author_detail'),
    (r'^(?P<author_slug>[-\w]+)/works/$', # Can be indexed
        work_list, {}, 'catalogue_author_list'),
    (r'^(?P<author_slug>[-\w]+)/works/search/$', # Shouldn't be indexed
        work_search, {}, 'catalogue_author_search'),
    (r'^(?P<author_slug>[-\w]+)/work-vote/(?P<work_slug>[-\w]+)/$',
        work_vote, {}, 'catalogue_work_vote'),
    (r'^(?P<author_slug>[-\w]+)/work/(?P<work_slug>[-\w]+)/$',
        work_detail, {}, 'catalogue_work_detail'),

    # Service
    (r'^service/make-bid/$',
        service_make_bid, {}, 'service_make_bid'),

    (r'^$', home, {}, 'catalogue_home'),
)
