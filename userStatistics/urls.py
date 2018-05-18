from . import views
from django.urls import path, re_path

urlpatterns = [
    path('', views.statsAll, name='Games Stats')
]
urlpatterns += [
    path('all', views.statsAll, name='Games Stats')
]