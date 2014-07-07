# coding=utf-8
import os
import datetime
import shutil
from time import sleep
import traceback
from zipfile import ZipFile

from django.conf import settings

from .models import Exchange
from .models import EXCHANGE_STATUS_INIT, EXCHANGE_STATUS_UPLOAD, EXCHANGE_STATUS_IMPORT, \
    EXCHANGE_STATUS_QUERY, EXCHANGE_STATUS_QUERY_SUCCESS
from ..catalog.exchange import jobs


EXCHANGE_CHECKAUTH = u"""success
{}
{}"""

EXCHANGE_INIT = u"""zip={}
file_limit={}"""

EXCHANGE_FAILURE = u"failure"

EXCHANGE_PROGRESS = u"progress"

EXCHANGE_SUCCESS = u"success"


def get_mode_handler(request):
    handlers = {
        'checkauth': CheckAuthHandler,
        'init': InitHandler,
        'file': FileHandler,
        'import': ImportHandler,
        'query': QueryHandler,
        'success': SuccessHandler,
    }

    try:
        handler = handlers[request.GET['mode']]
    except KeyError:
        raise ValidationException(u"Неправильный режим работы в запросе")

    return handler


def run_exchange(request, exchange_backend):
    handler_class = get_mode_handler(request)
    handler = handler_class(request, exchange_backend)
    try:
        result = handler.run()
    except Exception:
        error_message = traceback.format_exc()
        result = EXCHANGE_FAILURE
        try:
            handler.log(error_message)
        except Exception:
            pass
    return result


def get_exchange_path(code):
    return os.path.join(settings.EXCHANGE1C_UPLOAD_PATH, code)


def clear_exchange_path(code):
    shutil.rmtree(get_exchange_path(code))


def should_clear_files_immediately():
    return not settings.EXCHANGE1C_DEBUG_FILES


def clear_exchanges(expiration_days=14):
    """Clear all echange records and uploaded files older than expiration_days."""
    expiration_date = datetime.datetime.now() - datetime.timedelta(days=expiration_days)
    for exchange in Exchange.objects.filter(date_start__lt=expiration_date):
        clear_exchange_path(exchange.code)
        exchange.delete()


def unpack_files(filedir, cleanup):
    for filename in os.listdir(filedir):
        if filename.endswith('.zip'):
            fullpath = os.path.join(filedir, filename)
            with ZipFile(fullpath) as f:
                f.extractall(filedir)
            if cleanup:
                os.remove(fullpath)
            yield filename


class ValidationException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super(ValidationException, self).__init__(msg)

    def __str__(self):
        return self.msg


class ExchangeHandler(object):
    def __init__(self, request, exchange_backend):
        self.exchange_backend = exchange_backend
        self.params = request.GET
        self.exchange = None

    def run(self):
        self.validate()
        result = self.handle()
        return result

    def validate(self):
        pass

    def handle(self):
        raise ValidationException(u"Неправильная конфигурация загрузки - вызван абстрактный базовый класс")

    def log(self, message):
        self.exchange.log(message)
        self.exchange.save()

    def status(self, status):
        self.exchange.status = status
        self.exchange.save()


class CheckAuthHandler(ExchangeHandler):
    def __init__(self, request, *args, **kwargs):
        super(CheckAuthHandler, self).__init__(request, *args, **kwargs)
        self.meta = request.META
        self.session = request.session

    def validate(self):
        super(CheckAuthHandler, self).validate()
        if not self.check_basic_auth():
            raise ValidationException(u"Неправильные логин или пароль")

    def handle(self):
        self.cookie = self.session.session_key
        if not self.cookie:
            self.session.save()
            self.cookie = self.session.session_key

        exchange_type = self.params['type']
        self.exchange = Exchange.objects.create(code=self.cookie, exchange_type=exchange_type)
        self.log(u"Аутентификация обмена с сайтом")
        return EXCHANGE_CHECKAUTH.format(settings.EXCHANGE1C_COOKIE_NAME, self.cookie)

    def check_basic_auth(self):
        username, password = self.get_basic_auth()
        return username == settings.EXCHANGE1C_USER and password == settings.EXCHANGE1C_PASSWORD

    def get_basic_auth(self):
        authentication = self.meta.get('HTTP_AUTHORIZATION', ' ')
        authmethod, auth = authentication.split(' ', 1)
        if 'basic' == authmethod.lower():
            return auth.strip().decode('base64').split(':', 1)
        else:
            return None, None


class BaseExchangeHandler(ExchangeHandler):
    def __init__(self, request, *args, **kwargs):
        super(BaseExchangeHandler, self).__init__(request, *args, **kwargs)
        self.cookie = request.COOKIES.get(settings.EXCHANGE1C_COOKIE_NAME)
        self.exchange = Exchange.objects.get(code=self.cookie)

    def validate(self):
        super(BaseExchangeHandler, self).validate()
        expected_type = self.exchange.exchange_type
        params_type = self.params['type']
        if expected_type != params_type:
            raise ValidationException(
                u"Неправильный тип запроса, ожидается {}, а получен {}".format(expected_type, params_type))


class InitHandler(BaseExchangeHandler):
    allow_zip = u"yes"
    chunk_size_kb = 1024

    def handle(self):
        self.log(u"Начало загрузки файлов, частями по {} КБ".format(self.chunk_size_kb))
        self.status(EXCHANGE_STATUS_INIT)
        return EXCHANGE_INIT.format(self.allow_zip, self.chunk_size_kb * 1024) # File size is 1GB


class FileHandler(BaseExchangeHandler):
    def __init__(self, request, *args, **kwargs):
        super(FileHandler, self).__init__(request, *args, **kwargs)

        self.filename = self.params['filename']

        self.filedir = get_exchange_path(self.cookie)
        if not os.path.exists(self.filedir):
            os.makedirs(self.filedir)
        self.filepath = os.path.join(self.filedir, self.filename)

        self.data = request.raw_post_data

    def handle(self):
        with open(self.filepath, 'ab' if os.path.exists(self.filepath) else 'wb') as file:
            file.write(self.data)

        self.log(u"Загружена часть файла {} размером {}".format(self.filename, len(self.data)))
        self.status(EXCHANGE_STATUS_UPLOAD)
        return EXCHANGE_SUCCESS


class ImportHandler(BaseExchangeHandler):
    def handle(self):
        status = jobs.get_status(self.cookie)
        if status is None:
            if self.exchange.status != EXCHANGE_STATUS_UPLOAD:
                # If not in upload state, probably have got double load, to avoid this just return success
                return EXCHANGE_SUCCESS

            jobs.queue(self.cookie)
            self.log(u"Загрузка поставлена в очередь выполнения")

            return "{}\n{}".format(EXCHANGE_PROGRESS, "started")
        elif status == jobs.STATUS_FINISHED:
            return EXCHANGE_SUCCESS
        elif status == jobs.STATUS_ERROR:
            return EXCHANGE_FAILURE
        else:
            sleep(10)
            return "{}\n{}".format(EXCHANGE_PROGRESS, status)


class QueryHandler(BaseExchangeHandler):
    def handle(self):
        self.log(u"Начало выгрузки данных о заказах")
        self.status(EXCHANGE_STATUS_QUERY)
        return self.exchange_backend()


class SuccessHandler(BaseExchangeHandler):
    def handle(self):
        self.log(u"Подтверждение приема данных о заказах")
        self.status(EXCHANGE_STATUS_QUERY_SUCCESS)

        self.exchange_backend()
        return EXCHANGE_SUCCESS


class DumbOkHandler(BaseExchangeHandler):
    def handle(self):
        return EXCHANGE_SUCCESS
