# home/urls.py
from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('carousel/save/', views.save_slide, name='save_slide'),
    path('carousel/delete/', views.delete_slide, name='delete_slide'),
]