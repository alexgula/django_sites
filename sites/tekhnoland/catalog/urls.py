from django.conf.urls import *
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from .views import Search, AddBasketItem, Basket, BasketSave,\
    OrderMake, OrderDetail, OrderDetailExcel, OrderList, Exchange,\
    UploadForm, UploadBasket, UploadSave

urlpatterns = patterns('',
    # Catalog Search
    (r'^search/$',
        Search.as_view(), {}, 'search'),

    (r'^basket/$',
        Basket.as_view(), {}, 'basket'),
    (r'^basket/save/$',
        BasketSave.as_view(), {}, 'basket_save'),

    (r'^upload/$',
        UploadForm.as_view(), {}, 'upload_form'),
    (r'^upload/basket/$',
        UploadBasket.as_view(), {}, 'upload_basket'),
    (r'^upload/basket/save/$',
        UploadSave.as_view(), {}, 'upload_basket_save'),

    (r'^order/$',
        OrderMake.as_view(), {}, 'order'),
    (r'^order/(?P<pk>[\d]+)/$',
        OrderDetail.as_view(), {}, 'order_detail'),

    (r'^order/(?P<pk>[\d]+)/excel/$',
        OrderDetailExcel.as_view(), {}, 'order_detail_excel'),

    (r'^order/all/$',
        OrderList.as_view(), {}, 'order_list'),

    (r'^service/basket/add/$',
        AddBasketItem.as_view(), {}, 'add_basket_item'),

    (r'^exchange/$',
        csrf_exempt(never_cache(Exchange.as_view())), {}, 'exchange'),

)
