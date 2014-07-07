# coding=utf-8

ORDER_STATUS_CREATED = 0
ORDER_STATUS_IN_PROGRESS = 1
ORDER_STATUS_READY = 2
ORDER_STATUS_DELIVERED = 3
ORDER_STATUS_CANCELLED = 10

ORDER_STATUS_CHOICES = (
    (ORDER_STATUS_CREATED, "Created"),
    (ORDER_STATUS_IN_PROGRESS, "In progress"),
    (ORDER_STATUS_READY, "Ready"),
    (ORDER_STATUS_DELIVERED, "Delivered"),
    (ORDER_STATUS_CANCELLED, "Cancelled"),
)

PAYMENT_TYPE_CASH = 0
PAYMENT_TYPE_CREDIT_CARD = 1
PAYMENT_TYPE_BANK = 2
PAYMENT_TYPE_LIQPAY = 3

PAYMENT_TYPE_CHOICES = (
    (0, "Cash"),
    #(1, "Credit Card"),
    (2, "Bank Transfer"),
    (3, "LiqPay"),
)
