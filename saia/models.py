# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from shoreacres import settings
from django.utils.text import slugify


class News(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    news = models.CharField(max_length=1024)
    poster = models.CharField(max_length=32, null=False, blank=False,
                              default="Shore Acres Improvement Association")

    def __str__(self):
        return u'%s' % self.news[:10]


class Tag(models.Model):
    name = models.CharField(unique=True, null=False,
                            blank=False, max_length=32)

    def get_filter(self):
        return slugify(self.name)

    def __str__(self):
        return u'%s' % self.name


class Events(models.Model):
    date = models.DateTimeField(
        null=False, blank=False, default=timezone.now())
    title = models.CharField(max_length=64, null=False, blank=False)
    description = models.CharField(max_length=1024, null=False, blank=False)
    img = models.ImageField(upload_to='static/uploads/%Y/%m/%d/',
                            null=False, blank=True, default=settings.DEFAULT_EVENT_IMG)
    tags = models.ManyToManyField(Tag)

    def get_tags_list(self):
        return ' '.join([t.get_filter() for t in self.tags.all()])

    def __str__(self):
        return u'%s' % self.title
