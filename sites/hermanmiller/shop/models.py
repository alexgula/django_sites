# coding=utf-8
import decimal
from django.contrib.auth import hashers
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

from catalog.models import Product
from .model_choices import ORDER_STATUS_CHOICES, PAYMENT_TYPE_CHOICES, ORDER_STATUS_CREATED
from shop.utils import normalize_phone, get_data_for_model


class CustomerManager(models.Manager):
    def create(self, **kwargs):
        password = hashers.make_password(kwargs.pop('password'))
        data_for_model = get_data_for_model(self.model, **kwargs)
        return super(CustomerManager, self).create(
            password=password,
            **data_for_model)

    def authenticate(self, login, password):
        customers = []

        phone = normalize_phone(login)
        if len(phone) > 0:
            try:
                customers = [self.get_query_set().get(phone=phone)]
            except Customer.DoesNotExist:
                pass

        if len(customers) == 0:
            customers = list(self.get_query_set().filter(email=login))
            if len(customers) == 0:
                return None

        for customer in customers:
            if customer.check_password(password):
                return customer
        return None


class Customer(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    phone = models.CharField(_("Phone"), max_length=50, unique=True)
    password = models.CharField(_('Password'), max_length=128)
    email = models.EmailField(_("Email"), blank=True)
    code = models.CharField(_("Code"), max_length=20, blank=True)
    contact = models.CharField(_("Contact"), max_length=100, blank=True)
    address = models.TextField(_("Address"), blank=True)

    objects = CustomerManager()

    def __unicode__(self):
        return u"{} ({})".format(self.name, self.phone)

    def save(self, *args, **kwargs):
        self.phone = normalize_phone(self.phone)
        return super(Customer, self).save(*args, **kwargs)

    def set_password(self, password):
        self.password = hashers.make_password(password)
        self.save(update_fields=['password'])

    def check_password(self, password):
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])

        return hashers.check_password(password, self.password, setter)

    def get_data(self):
        return {
            field.name: getattr(self, field.name)
            for field in self._meta.local_fields
            if field.name not in ['id', 'password']
        }

    def update_data(self, data):
        dirty = False
        for field in self._meta.local_fields:
            name = field.name
            if name in data:
                if name == 'password':
                    self.set_password(data[name])
                else:
                    setattr(self, name, data[name])
                dirty = True
        if dirty:
            self.save()


class OrderManager(models.Manager):
    def create(self, customer, data):
        order_data = data['order']
        cart_data = data['cart']
        payment_type = order_data.pop('payment_type')
        item_quantities = {int(item['id']): item['quantity'] for item in cart_data}
        products = Product.objects.filter(id__in=item_quantities.keys())

        data_for_model = get_data_for_model(self.model, **order_data)
        sum_eur = sum((product.price_eur * item_quantities[product.id] for product in products))
        sum_uah = sum((product.price_uah * item_quantities[product.id] for product in products))

        if sum_eur == 0 or sum_uah == 0:
            return None

        order = super(OrderManager, self).create(
            customer=customer,
            payment_type=int(payment_type['id']),
            sum_eur=sum_eur,
            sum_uah=sum_uah,
            **data_for_model)

        for product in products:
            order.items.create(
                product=product,
                title=product.title,
                price_eur=product.price_eur,
                price_uah=product.price_uah,
                quantity=item_quantities[product.id],
            )

        return order


class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True)

    name = models.CharField(_("Name"), max_length=100, blank=True)
    phone = models.CharField(_("Phone"), max_length=50)
    email = models.EmailField(_("Email"), blank=True)
    code = models.CharField(_("Code"), max_length=20, blank=True)
    contact = models.CharField(_("Contact"), max_length=100, blank=True)
    address = models.TextField(_("Address"), blank=True)

    payment_type = models.IntegerField(_("Payment type"), choices=PAYMENT_TYPE_CHOICES)
    sum_eur = models.DecimalField(_("Sum (EUR)"), max_digits=16, decimal_places=2)
    sum_uah = models.DecimalField(_("Sum (UAH)"), max_digits=16, decimal_places=2)
    comment = models.TextField(_("Comment"), blank=True)

    date = models.DateTimeField(_("Order date"), auto_now_add=True)
    status = models.IntegerField(_("Status"), choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CREATED)

    objects = OrderManager()

    class Meta:
        ordering = ['-id', ]

    def __unicode__(self):
        return _("#{} of {}. Client {}, ({:.2f} EUR)").format(self.pk, self.date.strftime('%Y-%m-%d %H:%M'),
                                                              self.name, self.sum_eur)

    def save(self, *args, **kwargs):
        self.phone = normalize_phone(self.phone)
        return super(Order, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return 'shop_order_detail', None, dict(pk=self.pk)

    @property
    def sum_without_pdv(self):
        return self.sum_uah / decimal.Decimal(1.2)

    @property
    def sum_of_pdv(self):
        return self.sum_uah * decimal.Decimal(0.2) / decimal.Decimal(1.2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    title = models.CharField(_("Title"), max_length=250)
    price_eur = models.DecimalField(_("Price (EUR)"), max_digits=15, decimal_places=2)
    price_uah = models.DecimalField(_("Price (UAH)"), max_digits=15, decimal_places=2)
    quantity = models.PositiveIntegerField(_("Quantity"))

    def __unicode__(self):
        return u"{} {}".format(self.title, self.order)

    @property
    def sum(self):
        return self.price_uah * self.quantity

    @property
    def price_without_pdv(self):
        return self.price_uah / decimal.Decimal(1.2)

    @property
    def sum_without_pdv(self):
        return self.price_without_pdv * self.quantity


class PaymentLiqPayManager(models.Manager):
    def create(self, order, data):
        return super(PaymentLiqPayManager, self).create(
            order=order,
            amount=decimal.Decimal(data['amount']),
            currency=data['currency'],
            public_key=data['public_key'],
            description=data['description'],
            status=data['status'],
            transaction_id=int(data['transaction_id']),
            sender_phone=data['sender_phone'])


class PaymentLiqPay(models.Model):
    order = models.ForeignKey(Order, related_name="liqpays")
    amount = models.DecimalField(_("Amount"), max_digits=16, decimal_places=2)
    currency = models.CharField(_("Currency"), max_length=3)
    public_key = models.CharField(_("Public Key"), max_length=20)
    description = models.CharField(_("Description"), max_length=200)
    status = models.CharField(_("LiqPay Status"), max_length=20)
    transaction_id = models.PositiveIntegerField(_("LiqPay Transaction Id"))
    sender_phone = models.CharField(_("LiqPay Phone"), max_length=20)

    objects = PaymentLiqPayManager()
