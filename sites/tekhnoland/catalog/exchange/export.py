# coding=utf-8
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.datetime_safe import datetime
from ...account.models import CustomerProfile
from ..models import Order
from ..model_choices import *


class BaseExporter(object):

    def __init__(self, full_export=None):
        self.full_export = full_export

    def build(self):
        """Return an XML element."""
        pass


class Exporter(BaseExporter):
    full_export = False
    model = None
    template_name = None

    def get_queryset(self):
        return self.model.objects.all()

    def get_working_queryset(self):
        return self.get_queryset().filter(export_state=EXPORT_STATE_PROCESSING)

    def get_context_data(self, queryset):
        return {'object_list': queryset}

    def pre_build(self):
        queryset = self.get_queryset()
        if not self.full_export:
            queryset = queryset.filter(export_state=EXPORT_STATE_CHANGED)
        queryset.update(export_state=EXPORT_STATE_PROCESSING)

    def build(self):
        """Build XML output and statistics."""
        self.pre_build()

        queryset = self.get_working_queryset().select_related()
        text = render_to_string(self.template_name, self.get_context_data(queryset))

        return text

    def post_build(self):
        self.get_working_queryset().update(export_state=EXPORT_STATE_UNCHANGED)


class OrderExporter(Exporter):
    model = Order
    template_name = 'catalog/export/order_list.xml'


class ClientExporter(Exporter):
    model = CustomerProfile
    template_name = 'catalog/export/client_list.xml'

    def get_queryset(self):
        queryset = super(ClientExporter, self).get_queryset()
        return queryset.filter(user__is_active=True).exclude(user__username='admin')


class BaseComplexExporter(BaseExporter):

    def __init__(self, full_export=None):
        super(BaseComplexExporter, self).__init__(full_export=full_export)

        self.exporters = {
            'orders': OrderExporter(full_export),
            'clients': ClientExporter(full_export),
        }


class ComplexExporter(BaseComplexExporter):
    template_name = 'catalog/export/export.xml'

    def build(self):
        context = {
            'current_date': datetime.now(),

            # Have to pass encoding because PyCharm auto detects encodind and encodes the template file into windows-1251
            'encoding': 'windows-1251',
        }

        for key, exporter in self.exporters.iteritems():
            context[key] = exporter.build()

        return render_to_string(self.template_name, context)


class ExporterSuccess(BaseComplexExporter):

    def build(self):
        if not settings.EXCHANGE1C_DEBUG_ORDERS:
            for exporter in self.exporters.itervalues():
                exporter.post_build()
