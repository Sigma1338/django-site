from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def tournaments(request):
    return render(request, 'tournaments.html')


def tournament_detail(request, slug):
    return render(request, 'tournament_detail.html')
