# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-01 19:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('saia', '0006_auto_20171101_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 1, 19, 15, 18, 590160, tzinfo=utc)),
        ),
    ]
