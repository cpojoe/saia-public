# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-02 13:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('saia', '0012_auto_20171102_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 2, 13, 1, 44, 423971, tzinfo=utc)),
        ),
    ]
