from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from navigation.views import HomeNavigationView
from catalog.views import CategoryListView, CategoryDetailView, ProductDetailView, ProductReviewView
from content.views import NewsListView, NewsDetailView, StaticPageView
from shop.views import LoginView, LogoutView, CartView, CustomerView,\
    OrderView, OrderListView , OrderDetailView, OrderLiqPayConfirmView, OrderInvoice
from search.views import SearchView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeNavigationView.as_view(), name='home'),

    url(r'^catalog/$', CategoryListView.as_view(), name='category_list'),
    url(r'^catalog/(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name='category_detail'),
    url(r'^catalog/(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)/$', ensure_csrf_cookie(ProductDetailView.as_view()), name='product_detail'),
    url(r'^catalog/(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)/review/$', ensure_csrf_cookie(ProductReviewView.as_view()), name='product_review'),

    url(r'^news/$', NewsListView.as_view(), name='news_list'),
    url(r'^news/(?P<pk>[\d]+)/$', NewsDetailView.as_view(), name='news_detail'),

    url(r'^shop/login/$', LoginView.as_view(), name='shop_login'),
    url(r'^shop/logout/$', LogoutView.as_view(), name='shop_logout'),
    url(r'^shop/cart/$', CartView.as_view(), name='shop_cart'),
    url(r'^shop/customer/$', CustomerView.as_view(), {}, name='shop_customer'),
    url(r'^shop/order/$', OrderView.as_view(), name='shop_order'),
    url(r'^shop/orders/$', OrderListView.as_view(), name='shop_order_list'),
    url(r'^shop/order/(?P<pk>[\d]+)/$', OrderDetailView.as_view(), name='shop_order_detail'),
    url(r'^shop/order/(?P<pk>[\d]+)/liqpay-confirm/$', csrf_exempt(OrderLiqPayConfirmView.as_view()), name='shop_order_liqpay_confirm'),
    url(r'^shop/order/(?P<pk>[\d]+)/invoice\.pdf$', OrderInvoice.as_view(), name='shop_order_invoice'),

    url(r'^search/', SearchView.as_view(), name='search'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^(?P<slug>[-\w]+)/$', StaticPageView.as_view(), name='static_page'),
)

# Media serve ONLY for dev server, in production this should be done by server
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
    urlpatterns += patterns('',
        (r'^(?P<path>(favicon.ico|favicon.png|robots.txt))$',
            'django.views.static.serve',
            {'document_root': settings.WWW_ROOT}),
    )
