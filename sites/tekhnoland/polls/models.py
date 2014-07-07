# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    question = models.CharField(u"Вопрос", max_length=200)
    active = models.BooleanField(u"Активность", default=True)
    create_date = models.DateTimeField(u"Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = u"опрос"
        verbose_name_plural = u"опросы"

    def __unicode__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=u"Опрос", )
    choice = models.CharField(u"Выбор", max_length=50)
    votes = models.IntegerField(u"Кол-во голосов", default=0)

    class Meta:
        verbose_name = u"вариант"
        verbose_name_plural = u"варианты"

    def __unicode__(self):
        return self.choice


class Answer(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=u"", )
    choice = models.ForeignKey(Choice, verbose_name=u"", )
    customer = models.ForeignKey(User, verbose_name=u"", )

    class Meta:
        unique_together = 'poll', 'customer'
        verbose_name = u"ответ"
        verbose_name_plural = u"ответы"

    def __unicode__(self):
        return u"{} - {} ({})".format(self.poll, self.choice, self.customer)
