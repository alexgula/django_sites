# coding=utf-8
import os

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.conf import settings

from .models import Place, PlaceType, Region, Track, REGION_TYPES
from .util import color_map
from ..navigation.models import StaticNode
from ..navigation.views import HomeNavigationMixin, NavigationListView, NavigationDetailView
from ..content.views import FeinCMSObjectTemplateResponseMixin
from picassoft.utils.models import filter_choice
from picassoft.utils.classviews import JSONResponseMixin

def region_type_node(region_type):
    return StaticNode(filter_choice(REGION_TYPES, region_type), 'region_list', kwargs=dict(type_slug=region_type))


class RegionList(HomeNavigationMixin, NavigationListView):
    context_object_name = 'regions'
    model = Region
    template_name = 'region_list.html'

    def get_queryset(self):
        self.region_type = self.kwargs.get('type_slug', None)
        regions = Region.objects.all()
        if self.region_type:
            try:
                # Just check if the parameter of the view is valid
                filter_choice(REGION_TYPES, self.region_type)
            except ObjectDoesNotExist:
                raise Http404("No region type matches this query: {}".format(self.region_type))
            regions = regions.filter(type=self.region_type)
        return regions

    def get_trail_nodes(self):
        trail = super(RegionList, self).get_trail_nodes()
        trail = trail + [StaticNode(_("Regions"), 'region_list_all')]
        if self.region_type:
            return trail + [region_type_node(self.region_type)]
        else:
            return trail


class RegionDetail(FeinCMSObjectTemplateResponseMixin, HomeNavigationMixin, NavigationDetailView):
    context_object_name = 'region'
    template_name = 'region_detail.html'

    def get_object(self):
        self.region_type = self.kwargs['type_slug']
        return get_object_or_404(Region, type=self.region_type, slug=self.kwargs['slug'])

    def get_trail_nodes(self):
        trail = super(RegionDetail, self).get_trail_nodes()
        trail = trail + [StaticNode(_("Regions"), 'region_list_all')]
        return trail + [region_type_node(self.region_type), self.object]


class PlaceList(HomeNavigationMixin, NavigationListView):
    context_object_name = 'places'
    template_name = 'place_list.html'

    def get_queryset(self):
        self.place_type = get_object_or_404(PlaceType, slug=self.kwargs['type_slug'])
        return Place.objects.filter(
            type__lft__gte=self.place_type.lft,
            type__rght__lte=self.place_type.rght,
            type__tree_id=self.place_type.tree_id,
        ).select_related()

    def get_trail_nodes(self):
        trail = super(PlaceList, self).get_trail_nodes()
        return trail + [self.place_type.get_ancestors(), self.place_type]

    def get_context_data(self, **kwargs):
        context = super(PlaceList, self).get_context_data(**kwargs)
        context['type'] = self.place_type
        return context


class PlaceDetail(HomeNavigationMixin, NavigationDetailView):
    context_object_name = 'place'
    template_name = 'place_detail.html'

    def get_object(self):
        return get_object_or_404(Place, type__slug=self.kwargs['type_slug'], slug=self.kwargs['slug'])

    def get_trail_nodes(self):
        trail = super(PlaceDetail, self).get_trail_nodes()
        return trail + [self.object.type.get_ancestors(), self.object.type, self.object]


class ServiceRegionMap(JSONResponseMixin, View):

    def get(self, request, **kwargs):
        context = color_map.build_color_data(os.path.join(settings.STATIC_SOURCE, 'adminmap', 'color.png'))
        return self.render_to_response(context)


class ServiceTourMap(JSONResponseMixin, View):

    def get(self, request, **kwargs):
        place_types = PlaceType.objects.all()
        places = Place.objects.select_related()

        def insert_breaks(name, max_len=15):
            words = name.split(" ")

            res = []
            acc = []
            acc_words_len = 0
            for word in words:
                # Very long words place on separate string, thus, close string for previous words, if exist
                if len(word) > max_len and acc_words_len > 0:
                    res.append(" ".join(acc))
                    acc = []
                    acc_words_len = 0

                acc.append(word)
                acc_words_len += len(word)
                if acc_words_len > max_len:
                    res.append(" ".join(acc))
                    acc = []
                    acc_words_len = 0
            res.append(" ".join(acc))

            return '<br/>'.join(res)

        def place_context(place):
            return {
                'name': insert_breaks(place.name),
                'url': place.get_absolute_url(),
                'lon': place.lon,
                'lat': place.lat
            }

        context = {place_type.slug: {
            'name': place_type.name,
            'places': [],
            'icon': unicode(place_type.icon)
        } for place_type in place_types}

        for place in places:
            if place.lon is not None and place.lat is not None:
                context[place.type.slug]['places'].append(place_context(place))

        return self.render_to_response(context)


class TrackList(HomeNavigationMixin, NavigationListView):
    context_object_name = 'tracks'
    model = Track
    template_name = 'track_list.html'

    def get_trail_nodes(self):
        trail = super(TrackList, self).get_trail_nodes()
        trail = trail + [StaticNode(_("Holiday tours"), 'track_list')]
        return trail


class TrackDetail(HomeNavigationMixin, NavigationDetailView):
    context_object_name = 'track'
    model = Track
    template_name = 'track_detail.html'

    def get_trail_nodes(self):
        trail = super(TrackDetail, self).get_trail_nodes()
        trail = trail + [StaticNode(_("Holiday tours"), 'track_list')]
        return trail + [self.object]
