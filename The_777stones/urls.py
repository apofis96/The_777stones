"""The_777stones URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import auth
from django.views.generic import RedirectView
from testapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += [
    path('testapp/', include('testapp.urls')),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
urlpatterns += [
    re_path(r'^$', RedirectView.as_view(url='/testapp/', permanent=True)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('game/', include('game.urls')),
]

urlpatterns += [
    path('stats/', include('userStatistics.urls')),
]
urlpatterns += [
    path('home/', views.home, name='Home'),
]
urlpatterns += [
    path('accounts/', include('social_django.urls', namespace='social')),
]
