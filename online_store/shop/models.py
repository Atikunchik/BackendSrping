import delivery as delivery
from django.db import models

from django.conf import settings
from django.db.models import ForeignKey
from django.utils.functional import cached_property
from account.models import CustomUser


class Order(models.Model):
    PICKUP = 'PICKUP'
    DELIVERY = 'DELIVERY'
    ORDER_TYPES = (
        (PICKUP, 'PICKUP'),
        (DELIVERY, 'DELIVERY')
    )

    UNKNOWN = 'UNKNOWN'
    CARD = 'CARD'
    CASH = 'CASH'
    PAYMENT_METHODS = (
        (UNKNOWN, 'Неизвестно'),
        (CARD, 'Картой'),
        (CASH, 'Наличными')
    )

    IN_PROCESS = 'IN_PROCESS'
    CANCELLED = 'CANCELLED'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    READY_FOR_DELIVERY = 'READY_FOR_DELIVERY'
    READY_FOR_PICKUP = 'READY_FOR_PICKUP'
    STATUSES = (
        (IN_PROCESS, 'В обработке'),
        (CANCELLED, 'Отменено'),
        (SUCCESS, 'Успешно'),
        (FAILED, 'Неуспешно'),
        (READY_FOR_PICKUP, 'READY_FOR_PICKUP'),
        (READY_FOR_DELIVERY, 'READY_FOR_DELIVERY')
    )

    user = models.ForeignKey(
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        to=CustomUser
    )
    customer_phone_number = models.CharField(
        max_length=12
    )
    total_amount = models.FloatField()
    status = models.CharField(
        max_length=30,
        choices=STATUSES,
        default=IN_PROCESS,
    )
    order_type = models.CharField(
        max_length=25,
        choices=ORDER_TYPES,
        default=PICKUP
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default=UNKNOWN
    )
    cancel_reason = models.TextField(
        blank=True,
        null=True
    )
    customer_email = models.EmailField(
        blank=True,
        null=True
    )
    delivery_destination = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)


class Category(models.Model):
    name = models.CharField()
    subcategory = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )


class Brand(models.Model):
    name = models.CharField(max_length=30)
    selling_categories = models.ManyToManyField(
        Category
    )


class Review(models.Model):
    rating = models.IntegerField()
    comment = models.TextField()


class Item(models.Model):

    category = models.ManyToManyField(
        Category
    )
    order = models.ManyToManyField(
        Order,
        related_name='items',
        null=True
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='items'
    )
    price = models.FloatField()
    discount = models.FloatField()
    average_rating = models.FloatField()
    comment = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )
