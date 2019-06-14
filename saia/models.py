# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from shoreacres import settings


class EmailList(models.Model):
    email = models.EmailField(null=False, default='test@test.com')

    def __str__(self):
        return u'%s' % self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    img = models.ImageField(upload_to='static/uploads/%Y/%m/%d/', null=True, blank=True, default=settings.DEFAULT_USER_IMG)
    first_name = models.CharField(max_length=256, null=False, blank=False, default='')
    last_name = models.CharField(max_length=256, null=False, blank=False, default='')
    house_number = models.CharField(max_length=8, null=True, blank=True)
    street = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=14, null=True, blank=True)
    directory_visible = models.BooleanField(default=False)
    email_list = models.BooleanField(default=False)

    is_president = models.BooleanField(default=False)
    is_vice_president = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)
    is_treasurer = models.BooleanField(default=False)
    is_director = models.BooleanField(default=False)

    stripe_customer_id = models.CharField(max_length=32, null=True, blank=True)
    payment_type = models.CharField(max_length=32, null=True, blank=True)
    next_due_date = models.DateTimeField(null=True, blank=True)
    boat_ramp = models.BooleanField(default=False, blank=True)
    boat_ramp_next_due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return u'%s' % self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Classified(models.Model):
    poster = models.ForeignKey('Profile', on_delete=models.DO_NOTHING, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    img1 = models.ImageField(upload_to='static/uploads/%Y/%m/%d/', null=True, blank=True)
    img2 = models.ImageField(upload_to='static/uploads/%Y/%m/%d/', null=True, blank=True)
    img3 = models.ImageField(upload_to='static/uploads/%Y/%m/%d/', null=True, blank=True)
    title = models.CharField(max_length=64, blank=False, null=False)
    description = models.CharField(max_length=4096, blank=False, null=False)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return u'%s' % self.title


class News(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    news = models.CharField(max_length=1024)
    poster = models.ForeignKey('Profile', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return u'%s' % self.news[:10]


class Events(models.Model):
    date = models.DateTimeField(null=False, blank=False, default=timezone.now())
    title = models.CharField(max_length=64, null=False, blank=False)
    description = models.CharField(max_length=1024, null=False, blank=False)
    img = models.ImageField(upload_to='static/uploads/%Y/%m/%d/', null=False, blank=True, default=settings.DEFAULT_EVENT_IMG)

    def __str__(self):
        return u'%s' % self.title
