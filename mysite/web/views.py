from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import ApplicationForm, TournamentForm
from .models import Application, Tournament


def home(request):
    published = Tournament.objects.filter(status='published')
    stats = {
        'tournaments': published.count(),
        'teams': Application.objects.values('team').distinct().count(),
        'players': Application.objects.aggregate(total=Sum('players_count'))['total'] or 0,
    }
    return render(request, 'home.html', {
        'tournaments': published[:3],
        'stats': stats,
    })


def tournaments(request):
    return render(request, 'tournaments.html', {
        'tournaments': Tournament.objects.filter(status='published'),
    })


def tournament_detail(request, slug):
    tournament = get_object_or_404(Tournament, slug=slug)
    applications_count = tournament.applications.count()
    return render(request, 'tournament_detail.html', {
        'tournament': tournament,
        'applications_count': applications_count,
        'free_places': max(tournament.team_limit - applications_count, 0),
    })


def tables(request):
    return render(request, 'tables.html')


def teams(request):
    return render(request, 'teams.html')


def apply(request):
    initial = {}
    tournament_id = request.GET.get('tournament')
    if tournament_id:
        initial['tournament'] = tournament_id

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()
            messages.success(request, f'Заявка команды «{application.team}» принята.')
            return redirect('league:apply_success', pk=application.pk)
    else:
        form = ApplicationForm(initial=initial)

    return render(request, 'apply.html', {
        'form': form,
        'tournaments': Tournament.objects.filter(status='published'),
    })


def apply_success(request, pk):
    application = get_object_or_404(Application.objects.select_related('tournament'), pk=pk)
    return render(request, 'apply_success.html', {'application': application})


def login(request):
    error = ''
    next_url = request.POST.get('next') or request.GET.get('next') or ''

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}
            ):
                return redirect(next_url)
            if user.is_staff:
                return redirect('league:panel')
            return redirect('league:account')
        error = 'Неверный e-mail или пароль. Попробуйте ещё раз.'

    return render(request, 'login.html', {'error': error, 'next': next_url})


def logout(request):
    auth_logout(request)
    return redirect('league:login')


@login_required(login_url='league:login')
def account(request):
    return render(request, 'account.html')


staff_required = user_passes_test(
    lambda user: user.is_active and user.is_staff,
    login_url='league:login',
)


@staff_required
def panel(request):
    action = request.POST.get('action')

    if request.method == 'POST' and action in ('approve', 'reject'):
        application = get_object_or_404(Application, pk=request.POST.get('application'))
        application.status = 'approved' if action == 'approve' else 'rejected'
        application.save(update_fields=['status'])
        messages.success(
            request,
            f'Заявка команды «{application.team}» '
            f'{"одобрена" if action == "approve" else "отклонена"}.',
        )
        return redirect('league:panel')

    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.status = 'published' if request.POST.get('action') == 'publish' else 'draft'
            tournament.save()
            messages.success(request, f'Турнир «{tournament.title}» сохранён.')
            return redirect('league:panel')
        messages.error(request, 'Проверьте форму: есть ошибки.')
    else:
        form = TournamentForm()

    applications = list(Application.objects.select_related('tournament'))
    applications.sort(key=lambda item: item.status != 'pending')

    counts = {
        row['status']: row['total']
        for row in Application.objects.values('status').annotate(total=Count('id'))
    }

    statuses = {
        'pending': counts.get('pending', 0),
        'approved': counts.get('approved', 0),
        'rejected': counts.get('rejected', 0),
        'draft': counts.get('draft', 0),
    }

    stats = {
        'new_applications': statuses['pending'],
        'tournaments': Tournament.objects.count(),
        'teams': Application.objects.values('team').distinct().count(),
        'players': Application.objects.aggregate(total=Sum('players_count'))['total'] or 0,
    }

    return render(request, 'admin_panel.html', {
        'form': form,
        'applications': applications,
        'statuses': statuses,
        'stats': stats,
    })
