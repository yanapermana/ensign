# -*- coding: utf-8 -*-
# Generated by Django 1.9c1 on 2016-07-10 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0020_auto_20160710_0854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation',
            name='correct',
        ),
        migrations.AddField(
            model_name='evaluation',
            name='answer',
            field=models.CharField(default='A', max_length=1),
        ),
    ]
