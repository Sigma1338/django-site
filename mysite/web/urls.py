from django.urls import path

from . import views

app_name = 'league'

urlpatterns = [
    path('', views.home, name='home'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('tournaments/<slug:slug>/', views.tournament_detail, name='tournament_detail'),
    path('tables/', views.tables, name='tables'),
    path('teams/', views.teams, name='teams'),
    path('apply/', views.apply, name='apply'),
    path('apply/success/<int:pk>/', views.apply_success, name='apply_success'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('account/', views.account, name='account'),
    path('panel/', views.panel, name='panel'),
]
