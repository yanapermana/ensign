# -*- coding: utf-8 -*-
# Generated by Django 1.9c1 on 2016-07-12 12:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_evsolv_tries'),
    ]

    operations = [
        migrations.AddField(
            model_name='evsolv',
            name='attempt',
            field=models.BooleanField(default=False),
        ),
    ]
