# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-01 21:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('saia', '0007_auto_20171101_1915'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=256, null=True)),
                ('phone', models.CharField(blank=True, max_length=14, null=True)),
                ('directory_visible', models.BooleanField(default=False)),
                ('is_president', models.BooleanField(default=False)),
                ('is_vice_president', models.BooleanField(default=False)),
                ('is_secretary', models.BooleanField(default=False)),
                ('is_treasurer', models.BooleanField(default=False)),
                ('is_officer', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='events',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 1, 21, 54, 30, 85075, tzinfo=utc)),
        ),
    ]
