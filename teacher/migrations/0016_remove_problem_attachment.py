# -*- coding: utf-8 -*-
# Generated by Django 1.9c1 on 2016-07-08 19:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0015_auto_20160708_1904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='attachment',
        ),
    ]