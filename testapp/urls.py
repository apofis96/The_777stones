from django.conf.urls import url

from . import views
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls import include


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterFormView.as_view(), name="sign_up"),
    path('games/all', views.allGames, name='allGames')

]