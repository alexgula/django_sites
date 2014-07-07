# coding=utf-8
from django import http
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from picassoft.utils.classviews import JSONRequestMixin, JSONResponseMixin
from navigation.views import StaticNode, HomeNavigationView, NavigationListView, NavigationDetailView
from .email import EmailMixin
from . import session, liqpay, pdf, model_choices
from .models import Customer, Order, PaymentLiqPay


class CustomerLoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if session.auth.is_authenticated(self.request):
            return super(CustomerLoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        return http.HttpResponseRedirect(reverse('home'))


class CartView(View, JSONRequestMixin):
    def post(self, request, *args, **kwargs):
        cart_data = self.parse_request()
        session.cart.set_data(self.request, cart_data)
        return http.HttpResponse()


class LoginView(View, JSONRequestMixin, JSONResponseMixin):
    def post(self, request, *args, **kwargs):
        login_data = self.parse_request()
        customer = Customer.objects.authenticate(login_data['login'], login_data['password'])

        if customer is None:
            return http.HttpResponseForbidden()

        session.auth.set_data(self.request, customer)
        order_data = session.cart.update_order_data(self.request, customer.get_data())
        return self.render_to_response({'order': order_data})


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        session.auth.clear_data(self.request)
        return http.HttpResponse()


class CustomerView(View, JSONRequestMixin):
    def post(self, request, *args, **kwargs):
        """Create customer. Automatically logins."""
        customer_data = self.parse_request()
        customer = Customer.objects.create(**customer_data)
        session.auth.set_data(self.request, customer)
        return http.HttpResponse()

    def put(self, request, *args, **kwargs):
        """Update customer fields. 404 if not logged in.
        If want to set password, old password has to be provided in 'password_old' parameter."""
        customer = session.auth.get_data(self.request)
        if customer is None:
            return http.HttpResponseForbidden()

        password_old = kwargs.pop('password_old', None)
        password = kwargs.get('password', None)
        if password is not None and (password_old is None or not customer.check_password(password_old)):
            return http.HttpResponseForbidden()

        customer.update_data(**kwargs)
        session.auth.set_data(self.request, customer)
        return http.HttpResponse()


class OrderView(View, JSONRequestMixin, EmailMixin):
    def post(self, request, *args, **kwargs):
        cart_data = self.parse_request()
        session.cart.set_data(self.request, cart_data)

        customer = session.auth.get_data(self.request)
        if customer is None:
            password = cart_data.get('password', None)
            if password is not None:
                # if not logged in and password is provided - create a customer
                # if no password provided - create customerless order
                with transaction.commit_manually():
                    try:
                        customer = Customer.objects.create(password=password, **cart_data['order'])
                        transaction.commit()
                    except IntegrityError:
                        transaction.rollback()
                        return http.HttpResponseForbidden(_("Cannot create customer: duplicate phone"))

                session.auth.set_data(self.request, customer)

        order = Order.objects.create(customer, cart_data)

        if order is None:
            return http.HttpResponseForbidden(_("Cannot make empty order"))

        session.cart.clear_cart_data(self.request)
        self.send_order_notification(order)
        return http.HttpResponse(order.get_absolute_url())


class OrderListView(CustomerLoginRequiredMixin, NavigationListView):
    model = Order
    trail_parent = HomeNavigationView
    trail = StaticNode(_("Orders"), 'shop_order_list')

    def get_queryset(self):
        customer = session.auth.get_data(self.request)
        return super(OrderListView, self).get_queryset().filter(customer=customer)


class OrderDetailView(CustomerLoginRequiredMixin, NavigationDetailView):
    model = Order
    trail_parent = OrderListView

    def get_queryset(self):
        customer = session.auth.get_data(self.request)
        return super(OrderDetailView, self).get_queryset().filter(customer=customer)

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['site'] = get_current_site(self.request)
        return context


class OrderLiqPayConfirmView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        if liqpay.verify_signature(data):
            order = Order.objects.get(pk=int(data['order_id']))
            PaymentLiqPay.objects.create(order, data)
            if data['status'] == 'success':
                order.status = model_choices.ORDER_STATUS_IN_PROGRESS
                order.save()
            return http.HttpResponse()
        else:
            return http.HttpResponseForbidden("Invalid signature")


class OrderInvoice(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        invoice = pdf.invoice(order)
        return http.HttpResponse(invoice, content_type='application/pdf')
