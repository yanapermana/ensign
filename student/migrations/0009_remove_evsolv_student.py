# -*- coding: utf-8 -*-
# Generated by Django 1.9c1 on 2016-07-12 13:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_evsolv_attempt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evsolv',
            name='student',
        ),
    ]
