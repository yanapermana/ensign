# -*- coding: utf-8 -*-
# Generated by Django 1.9c1 on 2016-07-08 17:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0008_auto_20160629_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='picture',
            field=models.FileField(default='storages/problem/default.jpg', upload_to='storages/problem'),
        ),
    ]
