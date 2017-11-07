# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import News, Events, Profile, EmailList

admin.site.register(News)
admin.site.register(Events)
admin.site.register(Profile)
admin.site.register(EmailList)