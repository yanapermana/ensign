# -*- coding: utf-8 -*-
# Generated by Django 1.9c1 on 2016-07-12 14:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_auto_20160712_1408'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['date_created']},
        ),
    ]