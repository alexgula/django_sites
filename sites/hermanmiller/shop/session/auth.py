# coding=utf-8
from .cart import clear_order_data
from ..models import Customer


def is_authenticated(request):
    return get_data(request) is not None


def get_data(request):
    customer_pk = request.session.get('shop.auth', None)
    if customer_pk is None:
        return None
    else:
        return Customer.objects.get(pk=customer_pk)


def set_data(request, customer):
    request.session['shop.auth'] = customer.pk


def _clear_auth_data(request):
    if 'shop.auth' in request.session:
        del request.session['shop.auth']


def clear_data(request):
    _clear_auth_data(request)
    clear_order_data(request)
