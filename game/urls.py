from django.conf.urls import url

from . import views
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls import include


urlpatterns = [
    path('', views.game, name='Game game'),
]
urlpatterns += [
    path('new', views.newGame, name='New Game'),
]
urlpatterns += [
    path('join', views.joinGame, name='Join Game'),
]
urlpatterns += [
    path('joinPrivate', views.joinPrivateGame, name='Join Private Game'),
]
urlpatterns += [
    path('play', views.playGame, name='Play Game'),
]
urlpatterns += [
    path('playMove', views.playMove, name='Play Move')
]