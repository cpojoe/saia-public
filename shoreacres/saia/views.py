# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import logout, authenticate, login
from .forms import UserCreationForm, AuthForm, ProfileForm, EmailListForm
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from saia.models import News, Events, Profile, EmailList, News, Classified
from django.contrib.auth.decorators import login_required
from shoreacres import settings
import stripe
import json
from django.core.mail import EmailMultiAlternatives

def communityinfo(request):
    return render(request, 'community_info.html')

def board(request):
    profiles = Profile.objects.filter(is_director=True).order_by('last_name')
    context = {
        'title' : 'board of directors',
        'icon' : 'gavel',
        'profiles' : profiles
    }
    return render(request, 'directory.html', context)

def officers(request):
    president = Profile.objects.get(is_president=True)
    vpresident = Profile.objects.get(is_vice_president=True)
    secretary = Profile.objects.get(is_secretary=True)
    treasurer = Profile.objects.get(is_treasurer=True)
    context = {
        'president': president,
        'vpresident': vpresident,
        'secretary': secretary,
        'treasurer': treasurer
    }
    return render(request, 'officers.html', context)

@login_required
def directory(request):
    profiles = Profile.objects.filter(directory_visible=True).order_by('last_name')
    context = {
        'profiles' : profiles,
        'title' : 'neighborhood directory',
        'icon': 'users',
    }
    return render(request, 'directory.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user.profile)
        if form.is_valid():
            p = form.save()

            if 'directory_visible' in request.POST and request.POST['directory_visible'] == 'on':
                p.directory_visible = True
            else:
                p.directory_visible = False
            if 'email_list' in request.POST and request.POST['email_list'] == 'on':
                try:
                    em = EmailList.objects.get(email=p.email)
                except:
                    em = EmailList.objects.create(email=p.email)
                    em.save()
                p.email_list = True
            else:
                try:
                    em = EmailList.objects.get(email=p.email)
                    em.delete()
                except:
                    pass
                p.email_list = False
            p.save()
            return render(request, "profile_success.html")

    form = ProfileForm(instance=request.user.profile)
    context = {
        'form': form,
        'title': 'edit',
        'icon': 'fa-pencil',
        'btn': 'Update'
    }
    return render(request, 'gen_form.html', context)

def index(request):
    news = News.objects.all().order_by('-id')[:4]
    events = Events.objects.filter(date__gt=timezone.now()).order_by('date')[:4]
    context = {
        'news' : news,
        'events' : events,
    }
    return render(request, 'index.html', context)


def login_user(request):
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            login(request, user)
            return redirect('index')
    else:
        form = AuthForm()
    context = {
        'form': form,
        'title': 'login',
        'icon': 'fa-sign-in',
        'btn' : 'Log In',
    }
    return render(request, 'gen_form.html', context)

def logout_user(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    context = {
        'form' : form,
        'title' : 'register',
        'icon' : 'fa-user-plus',
        'btn' : 'Sign Up',
    }
    return render(request, 'gen_form.html', context)


def about(request):
    title = 'About Shore Acres'
    icon = 'fa-coffee'
    context = {
        'title' : title,
        'icon' : icon,
    }
    return render(request, 'about.html', context)


def facilities_info(request):
    return render(request, 'fac_info.html')

def facilities_sign(request):
    return render(request, 'fac_announcement.html')

def facilities_beach(request):
    return render(request, 'fac_beach.html')

def facilities_boatramp(request):
    return render(request, 'fac_boatramp.html')

def facilities_clubhouse(request):
    return render(request, 'fac_clubhouse.html')

def facilities_recreationarea(request):
    return render(request, 'fac_recreationarea.html')

def events(request):
    events = Events.objects.filter(date__gt=timezone.now()).order_by('date')
    return render(request, 'events.html', {'events': events})

def contact(request):
    return render(request, 'contact.html')

@login_required
def dues(request):
    #stripe.setPublishableKey(settings.STRIPE_PUBLIC_KEY)
    if not request.user.profile.stripe_customer_id:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        c = stripe.Customer.create()
        p = request.user.profile
        p.stripe_customer_id = c.id
        p.save()

    context = {'stripe_key': settings.STRIPE_PUBLIC_KEY}

    return render(request, 'dues.html', context)


def checkout(request):

    try:
        print 'EMAIL1', request.POST['stripeEmail'], request.user.profile.email
        profile = Profile.objects.get(email=request.POST['stripeEmail'])
        if request.POST['stripeEmail'] != request.user.profile.email:
            print 'EMAIL2', request.POST['stripeEmail'], request.user.profile.email
            raise Exception
    except:
        problems = ['Please sign up using the same e-mail address in your <a href="/edit/">profile</a>.',]
        context = {
            'problems': problems,
            'stripe_key': settings.STRIPE_PUBLIC_KEY
        }
        return render(request, 'dues.html', context)

    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        customer  = stripe.Customer.create(
            source=request.POST['stripeToken'],
            plan='annual',
            email=request.POST['stripeEmail']
            )
        print customer

    except stripe.error.CardError as ce:
        return False, ce

    else:
        return redirect("/thanks/")
        # The payment was successfully processed, the user's card was charged.
        # You can now redirect the user to another page or whatever you want


def thanks(request):
    return render(request, 'thanks.html')


def emailsignup(request):
    if request.method == 'POST':
        form = EmailListForm(data=request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                if request.POST['email'] != request.user.profile.email:
                    problem = 'Please sign up using the e-mail address listed in your <a href="/edit/">profile</a>.'
                    context = {
                        'problems': problem
                    }
                    return render(request, 'uhoh.html', context)
            try:
                e = EmailList.objects.get(email=request.POST['email'])
                problem = 'You are already signed up for our email list.'
                context = {
                    'problems': problem
                }
                return render(request, 'uhoh.html', context)
            except:
                e = EmailList.objects.create(email=request.POST['email'])
                e.save()
            try:
                p = Profile.objects.get(email=request.POST['email'])
                p.email_list = True
                p.save()
            except:
                pass
            return render(request, 'thanks_email.html')
    return redirect(request, '/')


@login_required
def addnews(request):
    p = request.user.profile
    if request.method == 'POST':
        if p.is_president or p.is_vice_president or p.is_secretary or p.is_secretary or p.is_director:
            try:
                if len(request.POST['news']) > 10:
                    n = News.objects.create(news=request.POST['news'])
                    n.save()
                    return render(request, 'news_success.html')
            except:
                problem = 'There was a problem with your news!'
                context = {
                    'problems': problem
                }
                return render(request, 'uhoh.html', context)

    if p.is_president or p.is_vice_president or p.is_secretary or p.is_secretary or p.is_director:
        return render(request, 'new_news.html')
    else:
        problem = 'You do not have permission to view this page.'
        context = {
            'problems': problem,
        }
        return render(request,'uhoh.html', context)

@login_required
def edit_positions(request):
    p = request.user.profile
    profiles = Profile.objects.all().order_by('last_name')
    if request.method == 'POST':
        if p.is_president or p.is_vice_president or p.is_secretary or p.is_secretary or p.is_director:
            c_pres = 0
            c_vp = 0
            c_sec = 0
            c_tre = 0
            for e in request.POST:
                if 'is_president' in e:
                    c_pres += 1
                if 'is_vice_president' in e:
                    c_vp += 1
                if 'is_secretary' in e:
                    c_sec += 1
                if 'is_treasurer' in e:
                    c_tre += 1
            problems = []
            if c_pres != 1:
                problems.append('You must select 1 President')
            if c_vp != 1:
                problems.append('You must select 1 Vice President')
            if c_sec != 1:
                problems.append('You must select 1 Secretary')
            if c_tre != 1:
                problems.append('You must select 1 Treasurer')
            if len(problems) > 0:
                context = {
                    'profiles': profiles,
                    'problems': problems,
                }
                return render(request, 'positions.html', context)

            for p in profiles:
                p.is_president = False
                p.is_vice_president = False
                p.is_secretary = False
                p.is_treasurer = False
                p.is_director = False
                p.save()

            for e in request.POST:
                if '_is_' in e:
                    ndx = e.index('_')
                    uid = int(e[:ndx])
                    p = Profile.objects.get(user=uid)
                    if 'is_president' in e:
                        p.is_president = True
                    elif 'is_vice_president' in e:
                        p.is_vice_president = True
                    elif 'is_secretary' in e:
                        p.is_secretary = True
                    elif 'is_treasurer' in e:
                        p.is_treasurer = True
                    elif 'is_director' in e:
                        p.is_director = True
                    p.save()

            problems = ['Positions updated successfully!',]
            profiles = Profile.objects.all().order_by('last_name')
            context = {
                'problems' : problems,
                'profiles' : profiles
            }
            return render(request, 'positions.html', context)

    if p.is_president or p.is_vice_president or p.is_secretary or p.is_secretary or p.is_director:
        context = {
            'profiles': profiles,
        }
        return render(request, 'positions.html', context)

    else:
        problem = 'You do not have permission to view this page.'
        context = {
            'problems': problem,
        }
        return render(request,'uhoh.html', context)


@login_required
def emailblast(request):
    p = request.user.profile

    if request.method == 'POST':
        if p.is_president or p.is_vice_president or p.is_secretary or p.is_secretary or p.is_director:
            try:
                message = request.POST['body']
                message += '\n\nTo unsubscribe from the Shore Acres email list, you can '
                html_message = message.replace('\n','<br>') + '<a href="' + settings.UNSUBSCRIBE_URL + '">click here</a> or '
                html_message += 'visit ' + settings.UNSUBSCRIBE_URL + ' from your browser.'
                message += 'visit ' + settings.UNSUBSCRIBE_URL + ' from your browser.'
                subject = request.POST['subject'].replace('\n','')
                from_addr = settings.FROM_EMAIL
                subscribers = [x.email for x in EmailList.objects.all()]
                email = EmailMultiAlternatives(
                    subject,
                    message,
                    from_addr,
                    [from_addr,],
                    subscribers,
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)
                return render(request, 'emailblast.html')
            except Exception, e:
                print e
                problems = 'Something went wrong.'
                context = {
                    'problems': problems,
                }
                return render(request, 'uhoh.html', context)


    if p.is_president or p.is_vice_president or p.is_secretary or p.is_secretary or p.is_director:
        emailnum = len(EmailList.objects.all())
        context = {
            'emailnum': emailnum,
        }
        return render(request, 'emailblast.html', context)
    else:
        problem = 'You do not have permission to view this page.'
        context = {
            'problems': problem,
        }
        return render(request,'uhoh.html', context)


def submitevent(request):
    if request.method == 'POST':
        try:
            from_addr = request.POST['email']
            subject = request.POST['subject'].replace('\n','')
            message = 'From: ' + request.POST['name'] + '\n'
            message += 'Email: ' + request.POST['email'] + '\n\n'
            message += request.POST['message']
            email = EmailMultiAlternatives(
                subject,
                message,
                from_addr,
                [settings.FROM_EMAIL,]
            )
            email.send()
            return render(request, 'submit_event_success.html')
        except:
            problems = 'Something went wrong.'
            context = {
                'problems': problems,
            }
            return render(request, 'uhoh.html', context)
    else:
        return render(request, '/')


@login_required
def classifieds(request):
    c = Classified.objects.all().order_by('-date')
    context = {
        'classifieds': c,
    }
    return render(request, 'classifieds.html', context)