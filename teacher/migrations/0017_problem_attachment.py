# -*- coding: utf-8 -*-
# Generated by Django 1.9c1 on 2016-07-08 19:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0016_remove_problem_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='attachment',
            field=models.FileField(default='static/media/problem/attachment/default.pcap', upload_to='static/media/problem/attachment'),
        ),
    ]
