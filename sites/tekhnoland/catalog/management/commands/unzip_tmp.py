# coding=utf-8
import os, logging
from django.conf import settings
from django.core.management.base import BaseCommand
from picassoft.utils.files import walk_files, extract_zip

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = u""
    help = u"""Unzip all zip files in '{}' directory""".format(settings.EXCHANGE1C_UPLOAD_DIR)

    def handle(self, *args, **options):
        count = 0
        for root, file_name in walk_files(os.path.join(settings.SITE_ROOT, settings.EXCHANGE1C_UPLOAD_PATH), '.zip'):
            extract_zip(os.path.join(root, file_name), root)
            count += 1
        logger.info(u"Successfully extracted {} files in {} directory.".format(count, settings.EXCHANGE1C_UPLOAD_DIR))
