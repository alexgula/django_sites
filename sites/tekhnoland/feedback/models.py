# coding=utf-8
from django.db import models
from picassoft.utils.views import permalink

FEEDBACK_CATEGORY_CHOICES = (
    ('order', u"Оплата"),
    ('select', u"Выбор товара"),
    ('delivery', u"Доставка"),
    ('payment', u"Оплата"),
    ('service', u"Сервисное обслуживание"),
    ('complaint', u"В отдел претензий"),
    ('site', u"Работа сайта"),
    ('other', u"Другое"),
)

FEEDBACK_STATUS_CHOICES = (
    ('client', u"Клиент"),
    ('partner', u"Партнер"),
    ('competitor', u"Конкурент"),
    ('guest', u"Гость"),
)


class Feedback(models.Model):
    category = models.CharField(u"Категория вопроса", max_length=10, choices=FEEDBACK_CATEGORY_CHOICES,
                                help_text=u"Выберите категорию вопроса из списка, чтоб мы смогли быстрее определить ответственных.")
    name = models.CharField(u"Ваше имя", max_length=100)
    email = models.EmailField(u"Ваш email")
    status = models.CharField(u"Ваш статус", max_length=10, choices=FEEDBACK_STATUS_CHOICES,
                                help_text=u"Выберите ваш статус из списка.")
    text = models.TextField(u"Текст сообщения")
    post_date = models.DateTimeField(u"Дата отправки", auto_now_add=True)

    class Meta:
        ordering = '-post_date',
        verbose_name = u"отзыв"
        verbose_name_plural = u"отзывы"
