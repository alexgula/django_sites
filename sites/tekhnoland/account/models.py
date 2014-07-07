# coding=utf-8
from random import random
import re
from hashlib import sha1 as sha_constructor
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from picassoft.utils.classutils import cached_property
from ..catalog.models import PriceType
from ..catalog.model_choices import EXPORT_STATE_CHOICES

SHA1_RE = re.compile('^[a-f0-9]{40}$')

def create_activation_key(username):
    salt = unicode(sha_constructor(str(random())).hexdigest()[:5])
    return sha_constructor(salt+username).hexdigest()

def get_expiration_date():
    """Find the date, after which registration date to be expired."""
    return datetime.now() - timedelta(days=settings.REGISTER_EXPIRATION_DAYS)


class RegistrationException(Exception):

    def __init__(self, registration, *args, **kwargs):
        super(RegistrationException, self).__init__(*args, **kwargs)
        self.registration = registration


class ExpiredRegistrationException(RegistrationException):

    def __unicode__(self, *args, **kwargs):
        return u"Время регистрации пользователя {} истекло, повторите, пожалуйста, процедуру регистрации".format(self.registration)


class ActivationKeyException(Exception):

    def __init__(self, activation_key, *args, **kwargs):
        super(ActivationKeyException, self).__init__(*args, **kwargs)
        self.activation_key = activation_key


class InvalidActivationKeyException(ActivationKeyException):

    def __unicode__(self, *args, **kwargs):
        return u"Ключ регистрации {} сформирован некорректно.".format(self.activation_key)


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=u"Пользователь")
    father_name = models.CharField(u"Отчество", max_length=30, blank=True, help_text=u"Не более 30 символов.")
    code1c = models.CharField(u"Код 1С", max_length=36, blank=True)
    username1c = models.CharField(u"Логин 1C", max_length=120, help_text=u"Не более 30 символов.")
    phone = models.CharField(u"Телефон", max_length=50, help_text=u"Не более 20 символов.")
    city = models.CharField(u"Город", max_length=150)
    address = models.TextField(u"Адрес", blank=True)
    delivery = models.TextField(u"Адрес доставки")
    price_type = models.ForeignKey(PriceType, verbose_name=u"Тип цены", blank=True, null=True)
    discount = models.DecimalField(u"Скидка", max_digits=16, decimal_places=4, blank=True, null=True, help_text=u"Размер скидки в %.")
    export_state = models.IntegerField(u"Состояние выгрузки", default=-1, choices=EXPORT_STATE_CHOICES, help_text=u"Служебное поле для использования во время выгрузки")

    def full_name(self):
        return self.username1c or self.user.get_full_name() or self.user.username

User.profile = cached_property('profile', lambda self: CustomerProfile.objects.get_or_create(user=self)[0])


class RegistrationManager(models.Manager):

    def activate(self, activation_key):
        if SHA1_RE.search(activation_key):
            try:
                registration = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                raise InvalidActivationKeyException(activation_key)
            if registration.activation_key_expired():
                raise ExpiredRegistrationException(registration)
            if not registration.activated:
                return self.create_inactive_user(registration)
        else:
            raise InvalidActivationKeyException(activation_key)

    def create_inactive_user(self, registration):
        user = User()
        user.username = registration.username
        user.email = registration.email
        user.password = registration.password
        user.last_name = registration.last_name
        user.first_name = registration.first_name
        user.is_staff = user.is_active = user.is_superuser = False
        user.date_joined = user.last_login = datetime.now()
        user.save()

        profile = CustomerProfile()
        profile.user = user
        profile.father_name = registration.father_name
        profile.username1c = registration.username1c
        profile.phone = registration.phone
        profile.city = registration.city
        profile.address = registration.address
        profile.delivery = registration.delivery
        profile.save()

        registration.activated = True
        registration.save()

        return user

    def delete_expired_registrations(self):
        self.filter(post_date__lte=get_expiration_date()).delete()


class Registration(models.Model):
    username = models.CharField(u"Логин", max_length=30, unique=True, help_text=u"Обязательное. Не более 30 символов. Латинские буквы, цифры и символы @.+-_.")
    password = models.CharField(u"Пароль", max_length=128, help_text=u"Обязательное. Не более 128 символов.")
    username1c = models.CharField(u"Логин 1C", max_length=120, unique=True, help_text=u"Обязательное. Не более 30 символов.")
    last_name = models.CharField(u"Фамилия", max_length=30, help_text=u"Обязательное. Не более 30 символов.")
    first_name = models.CharField(u"Имя", max_length=30, help_text=u"Обязательное. Не более 30 символов.")
    father_name = models.CharField(u"Отчество", max_length=30, blank=True, help_text=u"Не более 30 символов.")
    email = models.EmailField(u"Email", help_text=u"Обязательное. Не более 30 символов.")
    phone = models.CharField(u"Телефон", max_length=50, help_text=u"Обязательное. Не более 20 символов.")
    city = models.CharField(u"Город", max_length=150, help_text=u"Обязательное.")
    address = models.TextField(u"Адрес", blank=True)
    delivery = models.TextField(u"Адрес доставки", help_text=u"Обязательное.")
    source = models.TextField(u"Источник, откуда вы о нас узнали")
    post_date = models.DateTimeField(u"Дата регистрации", auto_now_add=True)
    activation_key = models.CharField(u"Ключ активации", max_length=40)
    activated = models.BooleanField(u"Активировано", default=False)

    objects = RegistrationManager()

    class Meta:
        verbose_name = u"регистрация"
        verbose_name_plural = u"регистрации"

    def __unicode__(self):
        return u"{} {} {} ({})".format(self.last_name, self.first_name, self.father_name, self.username)

    def clean(self):
        if not self.activation_key:
            self.activation_key = create_activation_key(self.username)

    def activation_key_expired(self):
        return self.post_date <= get_expiration_date()
    activation_key_expired.boolean = True
