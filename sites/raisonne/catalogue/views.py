# coding=utf-8
import datetime

import json
from decimal import Decimal
from django.contrib.sites.models import get_current_site
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.core import urlresolvers
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from localeurl.models import reverse
from .models import Author, Work, WorkLot
from .filters import build_filters, build_params, make_title
from ..ratings.views import rabid_rating
from ..views.generic.list_detail import object_list, object_detail
from picassoft.utils.profile import profile


CACHE_DURATION = 60 * 60

def catalog_urls(author_slug=None):
    if author_slug:
        search_url = reverse('catalogue_author_search', kwargs = {'author_slug': author_slug})
        list_url = reverse('catalogue_author_list', kwargs = {'author_slug': author_slug})
    else:
        search_url = reverse('catalogue_search')
        list_url = reverse('catalogue_list')
    return search_url, list_url

def redirect_to_search(request, author_slug=None):
    """Redirect to main site page.

    Cannot use django.views.generic.simple.redirect_to because localeurl
    uses monkey patching of django.core.urlresolvers.reverse only after
    building urls, so we need late reversing here.
    """
    if author_slug:
        return redirect('catalogue_author_list', author_slug=author_slug, permanent=True)
    else:
        return redirect('catalogue_list', permanent=True)

@cache_page(CACHE_DURATION)
def home(request):
    works = Work.objects.select_related()
    authors = Author.objects.filter(is_listed=True)
    search_url = urlresolvers.reverse('catalogue_search')
    filters = build_filters(build_params(request.GET))
    for filter in filters:
        filter.calc_facets(works, filters)
    return object_list(request, authors, template_name='catalogue/home.html', extra_context=dict(filters=filters, search_url=search_url))

@cache_page(CACHE_DURATION)
def content(request, template_name):
    works = Work.objects.select_related()
    search_url = urlresolvers.reverse('catalogue_search')
    filters = build_filters(build_params(request.GET))
    for filter in filters:
        filter.calc_facets(works, filters)
    template_names = [
        'static_content/{}_{}.html'.format(template_name, request.LANGUAGE_CODE),
        'static_content/{}.html'.format(template_name)
    ]
    return render_to_response(template_names, dict(filters=filters, search_url=search_url),
                              context_instance=RequestContext(request))

@profile('catalogue_search')
def _search(request, author_slug=None):
    works = Work.objects.filter(is_listed=True).select_related()
    template = 'catalogue/search.html'
    author = None

    query = request.GET.get('q', '')
    if query:
        works = works.filter(Q(name__icontains=query) | Q(desc__icontains=query))
    if author_slug:
        try:
            author = Author.objects.get(slug=author_slug)
        except Author.DoesNotExist:
            raise Http404
        works = works.filter(author__slug=author_slug)
        template = 'catalogue/author_search.html'

    search_url, list_url = catalog_urls(author_slug)

    filters = build_filters(build_params(request.GET), author_slug)
    works = works.distinct().order_by('name')
    for filter in filters:
        filter.calc_facets(works, filters)
    for filter in filters:
        works = works.filter(filter.build_query())
    filters_title = make_title(filters)

    template_vars = dict(author=author, filters_title=filters_title, works=works, filters=filters, search_url=search_url, list_url=list_url)
    return render(request, template, template_vars)

@cache_page(CACHE_DURATION)
def work_list(request, author_slug=None):
    # If use search engine indexable url and params are given, redirect to home search page.
    # This should halt search engines walks in filters combinations.
    for param in request.GET:
        if param != 'p':
            return redirect_to_search(request, author_slug)

    return _search(request, author_slug)

def work_search(request, author_slug=None):
    return _search(request, author_slug)

@cache_page(CACHE_DURATION)
def author_detail(request, author_slug):
    site = get_current_site(request)
    works = Work.objects.filter(author__slug=author_slug).select_related()

    authors = Author.objects.all()
    search_url, list_url = catalog_urls(author_slug)
    filters = build_filters(build_params(request.GET), author_slug)
    for filter in filters:
        filter.calc_facets(works, filters)

    template_vars = dict(filters=filters, search_url=search_url, list_url=list_url, site=site)
    return object_detail(request, queryset=authors, slug=author_slug, extra_context = template_vars)

@cache_page(CACHE_DURATION)
def work_detail(request, author_slug, work_slug):
    site = get_current_site(request)
    works = Work.objects.filter(author__slug=author_slug).select_related()

    search_url, list_url = catalog_urls(author_slug)
    filters = build_filters(build_params(request.GET), author_slug)
    for filter in filters:
        filter.calc_facets(works, filters)

    # Any work detail page access is considered a vote.
    try:
        Work.objects.get(author__slug=author_slug, slug=work_slug).vote()
    except Work.DoesNotExist:
        pass # No work (noun) - no work (verb) :)

    template_vars = dict(filters=filters, search_url=search_url, list_url=list_url, site=site)
    return object_detail(request, queryset=works, slug=work_slug, extra_context = template_vars)

@cache_page(CACHE_DURATION)
def lot_list(request, author_slug=None):
    works = Work.objects.select_related()

    search_url, list_url = catalog_urls(author_slug)

    filters = build_filters(build_params(request.GET), author_slug)
    for filter in filters:
        filter.calc_facets(works, filters)

    now = datetime.datetime.now()
    lots = WorkLot.objects.filter(is_open=True).filter(
        (Q(start_date__lte=now) & Q(close_date__gte=now)) | (Q(start_date__isnull=True) | Q(close_date__isnull=True))
    ).order_by('-close_date', 'work__name')

    template_names = [
        'static_content/auction_{}.html'.format(request.LANGUAGE_CODE),
        'static_content/auction.html'
    ]

    template_vars = dict(filters=filters, search_url=search_url, list_url=list_url, lots=lots)
    return render_to_response(template_names, template_vars,
                              context_instance=RequestContext(request))

@cache_page(CACHE_DURATION)
def lot_detail(request, author_slug, work_slug):
    works = Work.objects.filter(author__slug=author_slug).select_related()

    search_url, list_url = catalog_urls(author_slug)
    filters = build_filters(build_params(request.GET), author_slug)
    for filter in filters:
        filter.calc_facets(works, filters)

    lots = WorkLot.objects
    if request.user.is_authenticated():
        lots = lots.filter(work__author__slug=author_slug, work__slug=work_slug, is_open=True).order_by('-close_date')
    else:
        lots = lots.none()

    template_vars = dict(filters=filters, search_url=search_url, list_url=list_url)
    return object_detail(request, queryset=lots, object_id=lots[0].id, extra_context = template_vars)

@rabid_rating
def work_vote(request, author_slug, work_slug):
    work = Work.objects.get(author__slug=author_slug, slug=work_slug)
    work.vote(int(request.POST['vote']))
    return work.stars

@login_required
def service_make_bid(request):
    if request.method != 'POST':
        # For some silly bots
        return redirect_to_search(request)

    worklot_pk = int(request.POST['worklot_pk'])
    price = request.POST.get('price', None)
    res = {'message': u""}
    try:
        lot = WorkLot.objects.get(pk=worklot_pk)
        if price:
            price = Decimal(price.replace(',', '.'))
        lot.make_bid(request.user, price=price)
    except Exception, e:
        res['message'] = unicode(e)

    res['next_price'] = unicode(lot.next_price())
    res['bid_count'] = unicode(lot.bid_count())
    return HttpResponse(json.dumps(res))
