# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-09 02:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('saia', '0030_auto_20171108_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 9, 2, 27, 44, 992853, tzinfo=utc)),
        ),
    ]
