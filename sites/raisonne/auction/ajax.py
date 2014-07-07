# coding=utf-8
from dajaxice.core import dajaxice_functions
from dajax.core.Dajax import Dajax
from decimal import Decimal
from ..catalogue.models import WorkLot

def make_bid(request, parent_id, object_pk, price):
    dajax = Dajax()
    try:
        lot = WorkLot.objects.get(pk=object_pk)
        price = Decimal(price.replace(',', '.'))
        lot.make_bid(request.user, price=price)
        dajax.clear('#{} .message'.format(parent_id), 'innerHTML')
    except Exception, e:
        dajax.assign('#{} .message'.format(parent_id), 'innerHTML', e)

    dajax.assign('#{} .lot-next-price .price'.format(parent_id), 'innerHTML', lot.next_price())
    dajax.assign('#{} .lot-bid-count .count'.format(parent_id), 'innerHTML', lot.bid_count())
    return dajax.json()

dajaxice_functions.register(make_bid)
