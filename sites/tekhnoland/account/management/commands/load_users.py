# coding=utf-8
from time import time
import logging
from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from ...exchange import load_users

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = u"<file_name>"
    help = u"Load data from CSV file from old database."

    def handle(self, file_name, *args, **options):
        start = time()
        loaded, skipped, inserted = load_users(file_name)
        elapsed = time() - start

        logger.info(u"Successfully loaded file '{}'".format(file_name))
        logger.info(u"Loaded {} users in {} ({:.2f} users/s)".format(loaded, timedelta(seconds=elapsed), loaded / elapsed))
        logger.info(u"Skipped {}, inserted {} users)".format(skipped, inserted))
