# coding=utf-8
from django.shortcuts import get_object_or_404
from .models import Event, EVENT_TYPES
from ..navigation.models import StaticNode
from ..navigation.views import HomeNavigationMixin, NavigationListView, NavigationDetailView
from ..content.views import FeinCMSObjectTemplateResponseMixin
from datetime import date
import calendar
from picassoft.utils.classviews import JSONListView
from picassoft.utils.models import filter_choice
from django.views.generic.dates import YearMixin, MonthMixin, DayMixin, DateMixin

def normalize_month(year, month):
    """Remove month over- and underflow, like 13th or -2nd month etc.

    If month is zero, it counts as 12th month of previous year."""
    year, month = year + month / 12, month % 12
    if month == 0:
        year, month = year - 1, 12
    return year, month


def month_beginning(year, month):
    """Returns the first day of the given month."""
    year, month = normalize_month(year, month)
    return date(year, month, 1)


def month_ending(year, month):
    """Returns the last day of the given month."""
    year, month = normalize_month(year, month)
    return date(year, month, calendar.monthrange(year, month)[1])


def gen_calendar(year, month, events):
    days = dict()
    for date_from, date_to, data in events:
        period_from = max(date_from, month_beginning(year, month))
        period_to = min(date_to, month_ending(year, month))
        for day in xrange(period_from.day, period_to.day + 1):
            day_events = days.get(day, [])
            day_events.append(data)
            days[day] = day_events
    return days


class ServiceEventListByMonth(JSONListView):
    context_object_name = 'events'
    model = Event

    def get_queryset(self):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        date_from = month_beginning(year, month)
        date_to = month_beginning(year, month + 1)

        # Events which period intersects with the given period, not including it's upper bound.
        events = Event.objects.filter(active=True, type='event', date_to__gte=date_from, date_from__lt=date_to)
        return events

    def prepare_to_dump(self, obj):
        return {
            'name': obj.name,
            'desc': obj.desc,
            'date_from': obj.date_from.strftime('%Y-%m-%d'),
            'date_to': obj.date_to.strftime('%Y-%m-%d'),
        }

    def get_context_data(self, **kwargs):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        queryset = kwargs['object_list']

        context = super(ServiceEventListByMonth, self).get_context_data(**kwargs)
        context['calendar'] = gen_calendar(year, month, [(e.date_from, e.date_to, i) for i, e in enumerate(queryset)])
        return context


class TypedEventList(HomeNavigationMixin, NavigationListView):
    context_object_name = 'events'
    template_name = 'event_list.html'

    def get_queryset(self):
        self.event_type = self.kwargs['type_slug']
        return Event.objects.active().filter(type=self.event_type)

    def get_trail_nodes(self):
        trail = super(TypedEventList, self).get_trail_nodes()
        return trail + [
            StaticNode(filter_choice(EVENT_TYPES, self.event_type), 'typed_event_list', kwargs=dict(
                type_slug=self.event_type))
        ]

    def get_context_data(self, **kwargs):
        context = super(TypedEventList, self).get_context_data(**kwargs)
        context['slug'] = self.event_type
        context['type'] = filter_choice(EVENT_TYPES, self.event_type)
        return context


class PeriodEventList(DateMixin, TypedEventList):
    date_field = 'date_from'
    allow_future = True

    def get_queryset(self):
        events = super(PeriodEventList, self).get_queryset()
        self.date_from, self.date_to = self.get_period()
        events = events.filter(date_from__lt=self.date_to, date_to__gte=self.date_from).order_by('-date_to', '-date_from')
        return events


class EventListByYear(YearMixin, PeriodEventList):

    def get_period(self):
        year = int(self.get_year())
        date_from = date(year, 1, 1)
        date_to = date(year + 1, 1, 1)
        return date_from, date_to

    def get_trail_nodes(self):
        trail = super(EventListByYear, self).get_trail_nodes()
        return trail + [
            StaticNode(self.get_year(), 'event_list_by_year', kwargs=dict(
                type_slug=self.event_type,
                year=self.get_year(),
            ))
        ]

    def get_context_data(self, **kwargs):
        context = super(EventListByYear, self).get_context_data(**kwargs)
        context['year'] = self.get_year()
        return context


class EventListByMonth(MonthMixin, EventListByYear):
    month_format = '%m'

    def get_period(self):
        year = int(self.get_year())
        month = int(self.get_month())
        date_from = date(year, month, 1)
        date_to = self.get_next_month(date_from)
        return date_from, date_to

    def get_trail_nodes(self):
        trail = super(EventListByMonth, self).get_trail_nodes()
        return trail + [
            StaticNode(self.get_month(), 'event_list_by_month', kwargs=dict(
                type_slug=self.event_type,
                year=self.get_year(),
                month=self.get_month(),
            ))
        ]

    def get_context_data(self, **kwargs):
        context = super(EventListByMonth, self).get_context_data(**kwargs)
        context['month'] = self.get_month()
        return context


class EventListByDate(DayMixin, EventListByMonth):

    def get_period(self):
        year = int(self.get_year())
        month = int(self.get_month())
        day = int(self.get_day())
        date_from = date(year, month, day)
        date_to = self.get_next_day(date_from)
        return date_from, date_to

    def get_trail_nodes(self):
        trail = super(EventListByDate, self).get_trail_nodes()
        return trail + [
            StaticNode(self.get_day(), 'event_list_by_date', kwargs=dict(
                type_slug=self.event_type,
                year=self.get_year(),
                month=self.get_month(),
                day=self.get_day(),
            ))
        ]

    def get_context_data(self, **kwargs):
        context = super(EventListByDate, self).get_context_data(**kwargs)
        context['day'] = self.get_month()
        return context


class EventDetail(YearMixin, MonthMixin, DayMixin, FeinCMSObjectTemplateResponseMixin, HomeNavigationMixin, NavigationDetailView):
    context_object_name = 'event'

    def get_object(self):
        type_slug = self.kwargs['type_slug']
        year = int(self.get_year())
        month = int(self.get_month())
        day = int(self.get_day())
        date_from = date(year, month, day)
        slug = self.kwargs['slug']

        event = get_object_or_404(Event, type=type_slug, date_from=date_from, slug=slug, active=True)
        return event

    def get_trail_nodes(self):
        trail = super(EventDetail, self).get_trail_nodes()
        type_slug = self.object.type
        year, month, day = self.object.slug_date()
        return trail + [
            StaticNode(filter_choice(EVENT_TYPES, self.object.type), 'typed_event_list', kwargs=dict(
                type_slug=type_slug,
            )),
            StaticNode(self.get_year(), 'event_list_by_year', kwargs=dict(
                type_slug=type_slug,
                year=year,
            )),
            StaticNode(self.get_month(), 'event_list_by_month', kwargs=dict(
                type_slug=type_slug,
                year=year, month=month,
            )),
            StaticNode(self.get_day(), 'event_list_by_date', kwargs=dict(
                type_slug=type_slug,
                year=year, month=month, day=day,
            )),
            StaticNode(self.object, 'event_detail', kwargs=dict(
                type_slug=type_slug,
                year=year, month=month, day=day,
                slug=self.object.slug,
            )),
        ]
