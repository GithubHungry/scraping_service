from django.contrib import admin
from django.urls import path, include
from . import views

from . import views

urlpatterns = [
    path('list/', views.list_view, name='list'),
    path('', views.index, name='index'),
]
