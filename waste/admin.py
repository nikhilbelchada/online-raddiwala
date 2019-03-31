# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Waste


@admin.register(Waste)
class WasteAdmin(admin.ModelAdmin):
    pass

