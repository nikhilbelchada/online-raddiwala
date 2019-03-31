# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from waste_category.models import WasteCategory

class Waste(models.Model):
    waste_category = models.ForeignKey(WasteCategory, related_name="waste_category")
    name = models.CharField(max_length=50, blank=False)
    unit = models.CharField(max_length=50, blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
