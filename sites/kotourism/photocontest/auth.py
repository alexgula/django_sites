# coding=utf-8
from django.contrib.auth.models import check_password
from django.utils.functional import SimpleLazyObject
from .models import Author

AUTHOR_SESSION_KEY = '_author_id'


def author_login(request, author):
    request.session.set_test_cookie()
    request.session.cycle_key()
    request.session[AUTHOR_SESSION_KEY] = author.pk
    if hasattr(request, 'author'):
        request.author = author


def author_logout(request):
    del (request.session[AUTHOR_SESSION_KEY])
    request.session.cycle_key()
    if hasattr(request, 'author'):
        request.author = None


def author_authenticate(email, password):
    try:
        author = Author.objects.get(email=email)
    except Author.DoesNotExist:
        return None

    if not check_password(password, author.password):
        return None

    return author


def load_author(request):
    author_id = request.session.get(AUTHOR_SESSION_KEY, None)
    if author_id is None:
        return None

    try:
        return Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        return None


def get_author(request):
    if not hasattr(request, '_cached_author'):
        request._cached_author = load_author(request)
    return request._cached_author


class AuthorAuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request,
                       'session'), "The author authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

        request.author = SimpleLazyObject(lambda: get_author(request))


def context_processor(request):
    return {
        'author': getattr(request, 'author', None),
    }
