# coding=utf-8
import logging
from django.core.management.base import BaseCommand
from ...data_import import load_categories


class Command(BaseCommand):
    args = '<file_name>'
    help = 'Load data from XML file from 1C.'

    def handle(self, file_name, *args, **options):
        load_categories(file_name)
        logging.info('Successfully loaded file "{}"\n'.format(file_name))
