# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-24 10:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waste_category', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wastecategory',
            name='price',
        ),
    ]