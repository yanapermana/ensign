# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0027_problem_limited_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='limited_questions',
            field=models.CharField(max_length=2048, blank=True),
        ),
    ]
