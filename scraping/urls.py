from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.VacancyList.as_view(), name='list'),
    path('detail/<int:pk>/', views.VacancyDetail.as_view(), name='detail'),
    path('create/', views.VacancyCreate.as_view(), name='create'),
    path('update/<int:pk>/', views.VacancyUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', views.VacancyDelete.as_view(), name='delete'),
    path('', views.index, name='index'),
]
