# -*- coding: utf-8 -*-
# Generated by Django 1.9c1 on 2016-06-18 23:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_evaluation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suppot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('post', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Problem')),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
    ]
