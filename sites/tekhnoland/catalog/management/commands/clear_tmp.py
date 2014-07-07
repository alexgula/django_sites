# coding=utf-8
import os, logging, shutil, datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from picassoft.utils.files import old_dirs

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = u"[age]"
    help = u"""Clear subdirectories in '{}' directory, older that age in days, default age is {} days.""".format(settings.EXCHANGE1C_UPLOAD_DIR, settings.EXCHANGE1C_UPLOAD_RETENTION_DAYS)

    def handle(self, age=settings.EXCHANGE1C_UPLOAD_RETENTION_DAYS, *args, **options):
        count = 0
        for dir_path, is_old in old_dirs(os.path.join(settings.SITE_ROOT, settings.EXCHANGE1C_UPLOAD_PATH), datetime.timedelta(days=int(age))):
            if is_old:
                shutil.rmtree(dir_path)
                count += 1
        logger.info(u"Successfully deleted {} directories in {} directory.".format(count, settings.EXCHANGE1C_UPLOAD_DIR))
