from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.VacancyList.as_view(), name='list'),
    path('detail/<int:pk>/', views.VacancyDetail.as_view(), name='detail'),
    path('', views.index, name='index'),
]
