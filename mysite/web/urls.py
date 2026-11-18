from django.urls import path

from . import views

app_name = 'league'

urlpatterns = [
    path('', views.home, name='home'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('tournaments/<slug:slug>/', views.tournament_detail, name='tournament_detail'),
]
