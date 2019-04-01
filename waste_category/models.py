# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class WasteCategory(models.Model):
    """
    Waste Category Model
    Defines the attributes of a Waste Category
    """
    name = models.CharField(max_length=50, blank=False, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
