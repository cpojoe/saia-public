# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-09 02:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('saia', '0031_auto_20171109_0227'),
    ]

    operations = [
        migrations.AddField(
            model_name='classified',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 9, 2, 28, 22, 53812, tzinfo=utc)),
        ),
    ]
