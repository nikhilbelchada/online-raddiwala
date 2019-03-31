# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import WasteCategory


@admin.register(WasteCategory)
class WasteCategoryAdmin(admin.ModelAdmin):
    pass
