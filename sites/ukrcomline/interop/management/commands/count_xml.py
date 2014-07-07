# coding=utf-8
import collections
import logging
import six
from django.core.management.base import BaseCommand
from ...data_import import get_category_elems


class Command(BaseCommand):
    args = '<file_name>'
    help = 'Count unique attribute values from XML file from 1C.'

    def handle(self, file_name, *args, **options):
        attrs = collections.defaultdict(collections.Counter)
        for elem in get_category_elems(file_name):
            for attr in elem:
                attrs[attr.tag].update({attr.text: 1})

        for key, values in six.iteritems(attrs):
            logging.info(u"{}: {}".format(key, len(values)))
            #for value, cnt in six.iteritems(values):
            #    logging.info(u"  {}: {}".format(value, cnt))
