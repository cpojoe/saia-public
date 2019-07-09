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
    url(r'^about/$', saia_views.about, name="about"),
    url(r'^events/$', saia_views.events, name="events"),
    url(r'^contact/$', saia_views.contact, name="contact"),
    url(r'^clubhouse/$', saia_views.clubhouse, name="clubhouse"),
    url(r'^amenities/$', saia_views.amenities, name="amenities"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#handler404 = 'saia.views.index'
