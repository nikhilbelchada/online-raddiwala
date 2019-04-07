# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=10, blank=True)
    address = models.TextField(null=True)

    def user_details(self):
        return {
            'id': self.pk,
            'username': self.username,
            'email': self.email or "",
            'first_name': self.first_name or "",
            'last_name': self.last_name or "",
            'phone': self.phone or "",
            'admin': self.is_superuser or False,
            'address': self.address or "",
        }

    @property
    def is_admin(self):
        return self.is_superuser
