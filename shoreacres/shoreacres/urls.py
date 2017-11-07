"""shoreacres URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from saia import views as saia_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', saia_views.index, name="index"),
    url(r'^about/$', saia_views.about, name="about"),
    url(r'^facilities/info/$', saia_views.facilities_info, name="facilities_info"),
    url(r'^facilities/sign/$', saia_views.facilities_sign, name="facilities_sign"),
    url(r'^facilities/beach/$', saia_views.facilities_beach, name="facilities_beach"),
    url(r'^facilities/boatramp/$', saia_views.facilities_boatramp, name="facilities_boatramp"),
    url(r'^facilities/clubhouse/$', saia_views.facilities_clubhouse, name="facilities_clubhouse"),
    url(r'^facilities/recreationarea/$', saia_views.facilities_recreationarea, name="facilities_recreationarea"),
    url(r'^events/$', saia_views.events, name="events"),
    url(r'^contact/$', saia_views.contact, name="contact"),
    url(r'^login/$', saia_views.login_user, name="login"),
    url(r'^logout/$', saia_views.logout_user, name="logout"),
    url(r'^register/$', saia_views.register, name="register"),
    url(r'^edit/$', saia_views.edit_profile, name="edit_profile"),
    url(r'^directory/$', saia_views.directory, name="directory"),
    url(r'^officers/$', saia_views.officers, name="officers"),
    url(r'^board/$', saia_views.board, name="board"),
    url(r'^communityinfo/$', saia_views.communityinfo, name="communityinfo"),
    url(r'^dues/$', saia_views.dues, name="dues"),
    url(r'^checkout/$', saia_views.checkout, name="checkout_page"),
    url(r'^thanks/$', saia_views.thanks, name='thanks'),
    url(r'^emailsignup/$', saia_views.emailsignup, name='emailsignup'),
    url(r'^addnews/$', saia_views.addnews, name='addnews'),
    url(r'^editpositions/$', saia_views.edit_positions, name='editpositions'),
    url(r'^emailblast/$', saia_views.emailblast, name='emailblast'),
    url(r'^submitevent/$', saia_views.submitevent, name='submitevent')
]
