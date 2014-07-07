# coding=utf-8
from django.db import models
from datetime import datetime

EXCHANGE_TYPE_CHOICES = (
    ('catalog', u"Каталог"),
    ('sale', u"Заказы"),
)

EXCHANGE_STATUS_AUTH = 0
EXCHANGE_STATUS_INIT = 1
EXCHANGE_STATUS_UPLOAD = 2
EXCHANGE_STATUS_UNPACK = 3
EXCHANGE_STATUS_IMPORT = 4
EXCHANGE_STATUS_QUERY = 5
EXCHANGE_STATUS_QUERY_SUCCESS = 6
EXCHANGE_STATUS_IMPORT_SUCCESS = 7

EXCHANGE_STATUS_CHOICE = (
    (EXCHANGE_STATUS_AUTH, u"Аутентификация"),
    (EXCHANGE_STATUS_INIT, u"Инициализаця"),
    (EXCHANGE_STATUS_UPLOAD, u"Загрузка"),
    (EXCHANGE_STATUS_UNPACK, u"Распаковка"),
    (EXCHANGE_STATUS_IMPORT, u"Импорт в БД"),
    (EXCHANGE_STATUS_QUERY, u"Выгрузка с сайта"),
    (EXCHANGE_STATUS_QUERY_SUCCESS, u"Успех выгрузки"),
    (EXCHANGE_STATUS_IMPORT_SUCCESS, u"Успех импорта"),
)


class Exchange(models.Model):
    code = models.CharField(u"Код", max_length=40, unique=True)
    exchange_type = models.CharField(u"Тип обмена", max_length=7, choices=EXCHANGE_TYPE_CHOICES)
    date_start = models.DateTimeField(u"Дата и время старта", auto_now_add=True)
    status = models.IntegerField(u"Состояние обмена", choices=EXCHANGE_STATUS_CHOICE, default=EXCHANGE_STATUS_AUTH)
    messages = models.TextField(u"Сообщения", blank=True)

    class Meta:
        verbose_name = u"обмен"
        verbose_name_plural = u"обмены"
        ordering = '-date_start',

    def log(self, message):
        if message:
            message = u"[{}] {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message.strip())
            delim = u"-" * 40
            self.messages = u"\n".join([self.messages, delim, message])
