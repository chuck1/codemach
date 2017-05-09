"""web_sheets_django URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
import django.contrib.auth
import django.contrib.auth.views
from django.conf import settings
import django.urls
import django.shortcuts

import web_sheets_django.views

class LogoutView(django.contrib.auth.views.LogoutView):
    def get(self, request, *args, **kwargs):
        print('LogoutView')
        #url = django.urls.reverse('social:begin', args=['google-oauth2']) + '?next=' + django.urls.reverse('sheets:index')
        #return django.contrib.auth.views.logout_then_login(request, login_url=url)
        django.contrib.auth.logout(request)
        print('go to index')
        return django.shortcuts.redirect('index')


urlpatterns = [
        url(r'^$', web_sheets_django.views.IndexView.as_view(), name='index'),
        url(r'^sheets/', include('sheets_app.urls', namespace='sheets')),
        url(r'^admin/', admin.site.urls),
        url('', include('social_django.urls', namespace='social')),
        url(r'^logout/', LogoutView.as_view(), name='logout'),
]

if False:
	urlpatterns = [
		url(r'^sheets/', include(urlpatterns)),
	]

