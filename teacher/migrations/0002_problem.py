# -*- coding: utf-8 -*-
# Generated by Django 1.9c1 on 2016-06-18 23:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('attachment', models.CharField(max_length=255)),
                ('flag', models.CharField(max_length=255)),
                ('point', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Teacher')),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
    ]
