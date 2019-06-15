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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

# GARGBAGE
# this needs to get fixed eventually

urlpatterns = [
    url(r'^$', saia_views.index, name="index"),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', saia_views.login_user, name="login"),
    url(r'^logout/$', saia_views.logout_user, name="logout"),
    url(r'^register/$', saia_views.register, name="register"),
    url(r'^edit/$', saia_views.edit_profile, name="edit_profile"),
    url(r'^about/$', saia_views.about, name="about"),
    url(r'^board/$', saia_views.board, name="board"),
    url(r'^officers/$', saia_views.officers, name="officers"),
    url(r'^communityinfo/$', saia_views.communityinfo, name="communityinfo"),
    url(r'^news/$', saia_views.news, name='news'),
    url(r'^facilities/beach/$', saia_views.facilities_beach, name="facilities_beach"),
    url(r'^facilities/boatramp/$', saia_views.facilities_boatramp,
        name="facilities_boatramp"),
    url(r'^facilities/clubhouse/$', saia_views.facilities_clubhouse,
        name="facilities_clubhouse"),
    url(r'^facilities/info/$', saia_views.facilities_info, name="facilities_info"),
    url(r'^facilities/recreationarea/$',
        saia_views.facilities_recreationarea, name="facilities_recreationarea"),
    url(r'^facilities/sign/$', saia_views.facilities_sign, name="facilities_sign"),
    url(r'^events/$', saia_views.events, name="events"),
    url(r'^events/create/$', saia_views.create_event, name='create_event'),
    url(r'^contact/$', saia_views.contact, name="contact"),
    url(r'^directory/$', saia_views.directory, name="directory"),
    url(r'^dues/$', saia_views.dues, name="dues"),
    url(r'^unsubscribe/', saia_views.unsubscribe, name='unsubscribe'),
    url(r'^checkout/$', saia_views.checkout, name="checkout_page"),
    url(r'^thanks/$', saia_views.thanks, name='thanks'),
    url(r'^emailsignup/$', saia_views.emailsignup, name='emailsignup'),
    url(r'^addnews/$', saia_views.addnews, name='addnews'),
    url(r'^editpositions/$', saia_views.edit_positions, name='editpositions'),
    url(r'^emailblast/$', saia_views.emailblast, name='emailblast'),
    url(r'^submitevent/$', saia_views.submitevent, name='submitevent'),
    url(r'^classifieds/$', saia_views.classifieds, name='classifieds'),
    url(r'^classifieds/post/$', saia_views.postclassified, name='postclassified'),
    url(r'^classifieds/?(?P<id>[0-9]+)/$',
        saia_views.view_classified, name='view_classified'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#handler404 = 'saia.views.index'
