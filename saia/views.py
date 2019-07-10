import datetime
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from saia.models import News, Events


def index(request):
    title = 'Welcome'
    ns = News.objects.all().order_by('-id')[:4]
    time_thresh = timezone.now() - datetime.timedelta(hours=4)
    events = Events.objects.all().filter(date__gt=time_thresh).order_by('date')[:4]
    context = {
        'page_title': title,
        'news': ns,
        'events': events,
    }
    return render(request, 'index.html', context)


def about(request):
    title = 'About'
    context = {
        'page_title': title,
    }
    return render(request, 'about.html', context)


def events(request):
    title = 'Upcoming Events'
    time_thresh = timezone.now() - datetime.timedelta(hours=4)
    events = Events.objects.filter(date__gt=time_thresh).order_by('date')
    tags = []
    for e in events:
        tags += e.tags.all()
    context = {
        'page_title': title,
        'events': events,
        'tags': set(tags)
    }
    return render(request, 'events.html', context)


def contact(request):
    title = 'Contact'
    context = {
        'page_title': title,
    }
    return render(request, 'contact.html', context)


def clubhouse(request):
    title = 'Clubhouse'
    meta_description = 'The Shore Acres Clubhouse is a great family friendly party rental and meeting space located in Arnold, Maryland, near Annapolis and Severna Park.'
    context = {
        'page_title': title,
        'meta': meta_description
    }
    return render(request, 'clubhouse.html', context)


def amenities(request):
    title = 'Amenities'
    context = {
        'page_title': title,
    }
    return render(request, 'amenities.html', context)
