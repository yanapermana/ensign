# -*- coding: utf-8 -*-
# Generated by Django 1.9c1 on 2016-07-08 18:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0013_auto_20160708_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='picture_name',
        ),
    ]
