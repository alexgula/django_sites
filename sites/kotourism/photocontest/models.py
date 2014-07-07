# coding=utf-8
import re
from datetime import datetime, timedelta
from random import random
from hashlib import sha1 as sha_constructor
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField
from ..files.storage import HashedFileSystemStorage

SHA1_RE = re.compile('^[a-f0-9]{40}$')
HELPTEXT_REQUIRED = _("Required. Max {} characters.")

file_storage = HashedFileSystemStorage([2])


def is_key_valid(activation_key):
    return SHA1_RE.search(activation_key)


def create_activation_key(name):
    salt = unicode(sha_constructor(str(random())).hexdigest()[:5])
    return sha_constructor(salt+name).hexdigest()


def get_expiration_date():
    """Find the date, after which registration date to be expired."""
    return datetime.now() - timedelta(days=settings.AUTHOR_REGISTER_EXPIRATION_DAYS)


class RegistrationException(Exception):

    def __init__(self, registration, *args, **kwargs):
        super(RegistrationException, self).__init__(*args, **kwargs)
        self.registration = registration


class ExpiredRegistrationException(RegistrationException):

    def __unicode__(self, *args, **kwargs):
        return _("Activation for author {} is expired, you may repeat registration again").format(self.author)


class ActivationKeyException(Exception):

    def __init__(self, activation_key, *args, **kwargs):
        super(ActivationKeyException, self).__init__(*args, **kwargs)
        self.activation_key = activation_key


class InvalidActivationKeyException(ActivationKeyException):

    def __unicode__(self, *args, **kwargs):
        return _("Activation key {} is malformed or does not exist").format(self.activation_key)


class AuthorManager(models.Manager):

    def activate(self, activation_key):
        if is_key_valid(activation_key):
            try:
                author = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                raise InvalidActivationKeyException(activation_key)
            if author.activation_key_expired():
                raise ExpiredRegistrationException(author)
            author.activate()
        else:
            raise InvalidActivationKeyException(activation_key)

    def delete_expired_registrations(self):
        self.filter(post_date__lte=get_expiration_date()).delete()


class Author(models.Model):
    """Custom user type through custom authentication backend."""
    email = models.EmailField(_("E-mail"), max_length=254, unique=True, help_text=HELPTEXT_REQUIRED.format(254))
    password = models.CharField(_("Password"), max_length=128)
    name = models.CharField(_("Author Name"), max_length=250, help_text=HELPTEXT_REQUIRED.format(250))
    phone = models.CharField(_("Phone"), max_length=20, help_text=HELPTEXT_REQUIRED.format(20))
    post_date = models.DateTimeField(_("Registration date"), auto_now_add=True)
    active = models.BooleanField(_("Active"), default=False)
    activation_key = models.CharField(_("Activation key"), max_length=40)
    activated = models.BooleanField(_("Activated"), default=False)

    objects = AuthorManager()

    def __unicode__(self):
        return u"{} ({})".format(self.email, self.name)

    def clean(self):
        if not self.activation_key:
            self.activation_key = create_activation_key(self.email)

    def activate(self):
        self.active = True
        self.activated = True
        self.save()

    def activation_key_expired(self):
        return self.post_date <= get_expiration_date()
    activation_key_expired.boolean = True


class ContestManager(models.Manager):
    def active(self):
        """Return the last active contest or None if no active contest."""
        for contest in Contest.objects.filter(active=True).order_by('-date_to'):
            return contest
        return None


class Contest(models.Model):
    name = models.CharField(_("Name"), max_length=250)
    date_from = models.DateTimeField(_("Date From"))
    date_to = models.DateTimeField(_("Date To"))
    active = models.BooleanField(_("Active"), default=True)

    objects = ContestManager()

    def __unicode__(self):
        return u"{} ({} - {})".format(self.id, self.date_from, self.date_to)


class Photo(models.Model):
    author = models.ForeignKey(Author)
    contest = models.ForeignKey(Contest)
    name = models.CharField(_("Name"), max_length=50)
    image = ImageField(_("Image"), max_length=250, upload_to='photocontest', storage=file_storage)
    active = models.BooleanField(_("Active"), default=False)
    votes = models.PositiveIntegerField(_("Votes"), default=0)
    post_date = models.DateTimeField(_("Post Date"), auto_now_add=True)

    class Meta():
        unique_together = (('active', 'post_date'),)

    def __unicode__(self):
        return u"{} ({})".format(self.name, self.author)


class Vote(models.Model):
    photo = models.ForeignKey(Photo)
    post_date = models.DateTimeField(_("Post Date"), auto_now_add=True)
    address = models.GenericIPAddressField(_("IP Address"))

    class Meta():
        unique_together = (('photo', 'address', 'post_date'),)
