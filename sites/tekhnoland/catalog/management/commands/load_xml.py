# coding=utf-8
import logging
import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from picassoft.utils.filelock import FileLock, FileLockException
from picassoft.utils.profiling import timed_iterator
from ....exchange1c.exchange import get_exchange_path, clear_exchange_path, should_clear_files_immediately, unpack_files
from ....exchange1c.models import Exchange, EXCHANGE_STATUS_IMPORT_SUCCESS, EXCHANGE_STATUS_UNPACK, EXCHANGE_STATUS_IMPORT
from ...exchange.load import ProductLoader, ReplacementsLoader, ComplexOfferLoader, PendingLoader, ClientLoader, OrderLoader, import_files
from ...exchange import jobs

logger = logging.getLogger(__name__)

LOAD_TYPES = {
    'products': ProductLoader,
    'replacements': ReplacementsLoader,
    'offers': ComplexOfferLoader,
    'pending': PendingLoader,
    'clients': ClientLoader,
    'orders': OrderLoader,
}

LOAD_TYPES_DESC = u"\n".join(
    u"  {} -- {}".format(load_type, loader.__doc__) for load_type, loader in LOAD_TYPES.iteritems())

LOAD_TYPES_KEYS = u"|".join(LOAD_TYPES.iterkeys())


class InvalidLoadTypeError(CommandError):
    def __str__(self):
        return """Invalid load type. Possible values are:\n{}""".format(LOAD_TYPES_DESC)

    def __unicode__(self):
        return u"""Invalid load type. Possible values are:
        {}""".format(LOAD_TYPES_DESC)


class Command(BaseCommand):
    args = u"[({}) <file_name> | all <dir_name>]".format(LOAD_TYPES_KEYS)
    help = u"""Load data from a directory or from an XML file got from 1C.
    Types of loads:
    {}

    If parameters are empty, load files from a directory from a queue.""".format(LOAD_TYPES_DESC)

    def handle(self, load_type=None, file_name=None, *args, **options):
        try:
            with FileLock(settings.EXCHANGE1C_UPLOAD_PATH, timeout=10, delay=1):
                if load_type is None:
                    job_code = None
                    filedir = None
                    while True:
                        # If jobs are too old and no files are exist, quickly empty the queue
                        stop_processing, job_code = jobs.get()
                        if stop_processing:
                            return
                        if job_code is None:
                            continue
                        filedir = get_exchange_path(job_code)
                        if os.path.exists(filedir):
                            break

                    with jobs.run(job_code):
                        logger.info(u"Loading directory '{}'".format(job_code))
                        exchange = Exchange.objects.get(code=job_code)

                        exchange.status = EXCHANGE_STATUS_UNPACK
                        exchange.save()

                        packages = list(unpack_files(filedir, should_clear_files_immediately()))
                        for filename in packages:
                            exchange.log(u"Распакован файл {} в папку {}".format(filename, filedir))

                        exchange.status = EXCHANGE_STATUS_IMPORT
                        exchange.save()

                        for is_finished, filename, result in import_files(filedir, True):
                            if is_finished:
                                exchange.log(u"Обработан файл {}".format(filename))
                                exchange.log(result)
                                exchange.save()

                                logger.info(u"Successfully loaded file '{}'".format(filename))
                                logger.info(result)

                                jobs.set_status(job_code, 'loaded ' + filename)
                            else:
                                exchange.log(u"Начало обработки файла {}".format(filename))
                                exchange.save()

                                logger.info(u"Loading file '{}'".format(filename))
                                jobs.set_status(job_code, 'loading ' + filename)

                        if should_clear_files_immediately():
                            clear_exchange_path(job_code)

                        exchange.status = EXCHANGE_STATUS_IMPORT_SUCCESS
                        exchange.save()

                elif load_type == 'all':
                    logger.info(u"Loading directory '{}'".format(file_name))
                    filedir = get_exchange_path(file_name)

                    for is_finished, filename, result in import_files(filedir, False):
                        if is_finished:
                            logger.info(u"Successfully loaded file '{}'".format(filename))
                            logger.info(result)
                        else:
                            logger.info(u"Loading file '{}'".format(filename))
                else:
                    try:
                        loader = LOAD_TYPES[load_type]
                    except KeyError:
                        raise InvalidLoadTypeError()

                    for elapsed, stats in timed_iterator(loader(*args).load(file_name)):
                        for line in stats.format_with_time(elapsed):
                            logger.info(line)
                    logger.info(u"Successfully loaded file '{}'".format(file_name))
        except FileLockException:
            logger.info(u"Other task is active")
