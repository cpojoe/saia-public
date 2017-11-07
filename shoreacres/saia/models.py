# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class EmailList(models.Model):
    email = models.EmailField(null=False, default='test@test.com')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    img = models.ImageField(upload_to='static/uploads/%Y/%m/%d/', null=True, blank=True, default="/static/images/user.svg")
    first_name = models.CharField(max_length=256, null=False, blank=False, default='')
    last_name = models.CharField(max_length=256, null=False, blank=False, default='')
    email = models.EmailField(max_length=256, null=False, blank=False, default='')
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
    stripe_customer_id = models.CharField(max_length=32, null=True)
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

class News(models.Model):
    date = models.DateField(auto_now_add=True)
    news = models.CharField(max_length=1024)

class Events(models.Model):
    date = models.DateTimeField(null=False, blank=False, default=timezone.now())
    title = models.CharField(max_length=64, null=False, blank=False, default="New Event")
    description = models.CharField(max_length=1024)
    img = models.ImageField(upload_to='static/uploads/%Y/%m/%d/')