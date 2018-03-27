# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0026_evaluation_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='limited_questions',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
