# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_auto_20160725_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='writeup',
            name='teacher_point',
            field=models.IntegerField(default=0),
        ),
    ]
