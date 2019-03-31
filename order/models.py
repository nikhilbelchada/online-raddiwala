# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from waste.models import Waste
from raddi_user.models import User

STATUS_CREATED = 'CREATED'
STATUS_ACCEPTED = 'ACCEPTED'
STATUS_CANCELLED = 'CANCELLED'
STATUS_COMPLETE = 'COMPLETE'

STATUSES = (
    (STATUS_CREATED, 'Created'),
    (STATUS_ACCEPTED, 'Accepted'),
    (STATUS_CANCELLED, 'Cancelled'),
    (STATUS_COMPLETE, 'Complete'),
)


class Order(models.Model):
    user = models.ForeignKey(User)
    order_date = models.DateTimeField(auto_now_add=True)
    pickup_date = models.DateTimeField(null=True)
    status = models.CharField(choices=STATUSES, max_length=10, default=STATUS_CREATED)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    feedback = models.TextField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', null=True)
    waste = models.ForeignKey(Waste)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
