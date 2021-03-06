# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-07-02 21:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('saia', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classified',
            name='poster',
        ),
        migrations.DeleteModel(
            name='EmailList',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AlterField(
            model_name='events',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 2, 21, 5, 7, 77498, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='events',
            name='img',
            field=models.ImageField(blank=True, default=b'/static/images/event.jpg', upload_to='static/uploads/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='news',
            name='poster',
            field=models.CharField(default='Shore Acres Improvement Association', max_length=32),
        ),
        migrations.DeleteModel(
            name='Classified',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
