# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import News, Events, Tag

admin.site.register(Tag)
admin.site.register(News)
admin.site.register(Events)
