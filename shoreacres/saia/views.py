# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import json
import requests
import stripe
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from shoreacres import settings
from saia.models import News, Events, Profile, EmailList, News, Classified
from .forms import UserCreationForm, AuthForm, ProfileForm, EmailListForm, ClassifiedForm, EventForm


def communityinfo(request):
    return render(request, 'community_info.html')


def board(request):
    profiles = Profile.objects.filter(is_director=True).order_by('last_name')
    context = {
        'title' : 'board of directors',
        'icon' : 'gavel',
        'profiles' : profiles
    }
    return render(request, 'element_panels.html', context)


def officers(request):
    try:
        president = Profile.objects.get(is_president=True)
        vpresident = Profile.objects.get(is_vice_president=True)
        secretary = Profile.objects.get(is_secretary=True)
        treasurer = Profile.objects.get(is_treasurer=True)
        context = {
            'title': 'officers',
            'icon': 'institution',
            'profiles' : [president, vpresident, secretary, treasurer],
        }
    except:
        context = {
            'title' : 'officers',
            'icon': 'institution',
        }
    return render(request, 'element_panels.html', context)


@login_required
def directory(request):
    profiles = Profile.objects.filter(directory_visible=True).order_by('last_name')
    context = {
        'profiles' : profiles,
        'title' : 'neighborhood directory',
        'icon': 'users',
    }
    return render(request, 'element_panels.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':

        if 'ignore_file' not in request.POST:
            form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        else:
            form = ProfileForm(request.POST, instance=request.user.profile)
        
        if form.is_valid():
            p = form.save()

            if 'directory_visible' in request.POST and request.POST['directory_visible'] == 'on':
                p.directory_visible = True
            else:
                p.directory_visible = False

            if 'email_list' in request.POST and request.POST['email_list'] == 'on':

                try:
                    em = EmailList.objects.get(email=p.user.email)
                except:
                    em = EmailList.objects.create(email=p.user.email)
                    em.save()

                p.email_list = True

            else:

                try:
                    em = EmailList.objects.get(email=p.user.email)
                    em.delete()
                except:
                    pass

                p.email_list = False

            p.save()

            message = 'Your profile was updated successfully!'
            context = {
                'message': message,
            }

            return render(request, "thanks.html", context)

        else:
            context = {
                'form': form,
                'title': 'edit',
                'icon': 'fa-pencil',
                'btn': 'Update'
            }
            return render(request, 'gen_form.html', context)

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

def check_privs(request):
    p = request.user.profile
    status = False
    if p.is_president:
        status = True
    elif p.is_vice_president:
        status = True
    elif p.is_secretary:
        status = True
    elif p.is_treasurer:
        status = True
    elif p.is_director:
        status = True
    return status


@login_required
def create_event(request):
    if not check_privs(request):
        problem = 'You do not have permission to create events.'
        context = {
            'problems': problem,
        }
        return render(request, 'uhoh.html', context)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            message = 'Event created!</br><a href="/events/">Return to events page</a>'
            context = {
                'message': message,
            }
            return render(request, 'thanks.html', context)

    form = EventForm()
    context = {
        'form': form,
        'title': 'create event',
        'icon': 'fa-calendar-o',
        'btn': 'Create'
    }
    return render(request, 'gen_form.html', context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.user.is_authenticated:
        problem = 'You\'re already registered and logged in as %s.' % request.user.username
        context = {
            'problems': problem,
        }
        return render(request, 'uhoh.html', context)

    if request.method == 'POST':
        recaptcha = request.POST['g-recaptcha-response']
        params = {
            'secret': settings.RECAPTCHA_SECRET,
            'response': recaptcha,
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', params = params)
        resp = json.loads(r.content)

        if resp['success'] == True:
            form = UserCreationForm(data=request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                message = 'Registration successful.</br></br>'
                context = {
                    'message': message
                }
                return render(request, 'thanks.html', context)
            else:
                context = {
                    'form' : form,
                    'title' : 'register',
                    'icon' : 'fa-user-plus',
                    'btn' : 'Sign Up',
                }
                return render(request, 'gen_form.html', context)
        else:
            problem = 'Google thinks you\'re a robot. Sorry, this website is intended for humans.'
            context = {
                'problems': problem,
            }
            return render(request, 'uhoh.html', context)

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
    context = {
        'icon': 'calendar',
        'title': 'upcoming community events',
        'events': events,
    }
    return render(request, 'element_panels.html', context)

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
        print 'EMAIL1', request.POST['stripeEmail'], request.user.email
        profile = Profile.objects.get(email=request.POST['stripeEmail'])
        if request.POST['stripeEmail'] != request.user.email:
            print 'EMAIL2', request.POST['stripeEmail'], request.user.email
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
        message = 'Thank you for supporting our community!</br></br>Your payment was processed successfully!'
        context = {
            'message': message
        }
        return render(request, 'thanks.html', context)


def thanks(request):
    message = 'Thank you for supporting our community!</br></br>Your payment was processed successfully!'
    context = {
        'message': message
    }
    return render(request, 'thanks.html', context)


def emailsignup(request):
    if request.method == 'POST':
        form = EmailListForm(data=request.POST)
        if form.is_valid():
            if request.user.is_authenticated():
                if request.POST['email'] != request.user.email:
                    problem = 'Please sign up using the e-mail address listed in your <a href="/edit/">profile</a>.'
                    context = {
                        'problems': problem
                    }
                    return render(request, 'uhoh.html', context)
            try:
                e = EmailList.objects.get(email=request.POST['email'])
                if request.user.is_authenticated():
                    problem = 'You are already signed up for our email list.</br>To unsubscribe, <a href="/edit/">click here</a> and uncheck the </br>"Sign up for our email list?" box, then click submit.'
                else:
                    problem = 'You are already signed up for our email list.</br><a href="#">Click here</a> to unsubscribe.'
                context = {
                    'problems': problem
                }
                return render(request, 'uhoh.html', context)
            except:
                e = EmailList.objects.create(email=request.POST['email'])
                e.save()
            if request.user.is_authenticated():
                p = User.objects.get(email=request.POST['email']).profile
                p.email_list = True
                p.save()
            message = "Thanks! You are now added to our email list."
            context = {
                'message': message
            }
            return render(request, 'thanks.html', context)
    return redirect(request, '/')


@login_required
def addnews(request):
    status = check_privs(request)
    if not status:
        problem = 'You do not have permission to view this page.'
        context = {
            'problems': problem,
        }
        return render(request,'uhoh.html', context)

    p = request.user.profile
    if request.method == 'POST':
            try:
                if len(request.POST['news']) > 10:
                    n = News.objects.create(news=request.POST['news'], poster=request.user.profile)
                    n.save()
                    return render(request, 'news_success.html')
                else:
                    problem = 'Your news is too short. </br><a href="/addnews/">Go back</a>.'
                    context = {
                        'problems': problem,
                    }
                    return render(request, 'uhoh.html', context)

            except:
                problem = 'There was a problem with your news!'
                context = {
                    'problems': problem
                }
                return render(request, 'uhoh.html', context)

    return render(request, 'new_news.html')
    
@login_required
def edit_positions(request):
    status = check_privs(request)
    if not status:
        problem = 'You do not have permission to view this page.'
        context = {
            'problems': problem,
        }
        return render(request,'uhoh.html', context)

    p = request.user.profile
    profiles = Profile.objects.all().order_by('last_name')
    if request.method == 'POST':
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

    context = {
        'profiles': profiles,
    }
    return render(request, 'positions.html', context)



@login_required
def emailblast(request):
    status = check_privs(request)
    if not status:
        problem = 'You do not have permission to view this page.'
        context = {
            'problems': problem,
        }
        return render(request,'uhoh.html', context)

    p = request.user.profile

    if request.method == 'POST':
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


    emailnum = len(EmailList.objects.all())
    context = {
        'emailnum': emailnum,
    }
    return render(request, 'emailblast.html', context)


@login_required
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
            message = 'Your message was sent successfully!'
            context = {
                'message': message,
            }
            return render(request, 'thanks.html', context)
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
    classifieds = Classified.objects.filter(visible=True).order_by('-date')
    for c in classifieds:
        if c.date < (timezone.now() - datetime.timedelta(days=30)):
            c.visible = False
            c.save()
    classifieds = Classified.objects.filter(visible=True).order_by('-date')
    context = {
        'icon': 'newspaper-o',
        'title': 'classifieds', 
        'classifieds': classifieds,
    }
    return render(request, 'element_panels.html', context)


@login_required
def postclassified(request):
    if request.method == 'POST':
        print request.POST
        if 'ignore_file1' in request.POST and request.POST['ignore_file1'] == '0':
            request.FILES.pop('img1',None)
        if 'ignore_file2' in request.POST and request.POST['ignore_file2'] == '0':
            request.FILES.pop('img2', None)
        if 'ignore_file3' in request.POST and request.POST['ignore_file3'] == '0':
            request.FILES.pop('img3', None)
        if request.FILES:
            form = ClassifiedForm(request.POST, request.FILES)
        else:
            form = ClassifiedForm(data=request.POST)
        if form.is_valid():
            c = form.save()
            c.poster = request.user.profile
            c.save()
        else:
            context = {
                'errors': form.errors,
            }
            return render(request, 'post_classified.html', context)
        message = 'Your post was successful!</br><a href="/classifieds/">Click here</a> to return to the classifieds.'
        context = {
            'message': message
        }
        return render(request, 'thanks.html', context)
    return render(request, 'post_classified.html')


@login_required
def view_classified(request, id):
    classifieds = Classified.objects.filter(visible=True).order_by('-date')
    for c in classifieds:
        if c.date < (timezone.now() - datetime.timedelta(days=30)):
            c.visible = False
            c.save()
    try:
        c = Classified.objects.filter(visible=True).get(id=id)
    except:
        problem = 'That classified doesn\'t exist.'
        context = {
            'problems' : problem,
        }
        return render(request, 'uhoh.html', context)
    context = {
        'c': c,
    }
    return render(request,'classified.html',context)


def news(reqeust):
    n = News.objects.all().order_by('-date')[:24]
    context = {
        'title': 'recent news',
        'icon': 'newspaper-o',
        'news': n,
    }
    return render(reqeust, 'element_panels.html', context)