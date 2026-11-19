from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Application, Tournament


class PublicPagesTests(TestCase):
    def setUp(self):
        self.tournament = Tournament.objects.first()

    def test_main_pages_render(self):
        for name in ('league:home', 'league:tournaments', 'league:tables', 'league:teams', 'league:apply', 'league:login'):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)

    def test_tournament_detail_uses_slug(self):
        response = self.client.get(self.tournament.get_absolute_url())
        self.assertContains(response, self.tournament.title)

    def test_unknown_tournament_returns_404(self):
        response = self.client.get(reverse('league:tournament_detail', args=['no-such-tournament']))
        self.assertEqual(response.status_code, 404)

    def test_application_is_saved(self):
        response = self.client.post(reverse('league:apply'), {
            'tournament': self.tournament.pk,
            'team': 'Новая команда',
            'city': 'Ульяновск',
            'captain': 'Иванов Иван',
            'phone': '+7 900 111-22-33',
            'email': 'new@mail.ru',
            'players_count': 6,
            'comment': '',
            'consent': 'on',
        })
        application = Application.objects.get(team='Новая команда')
        self.assertRedirects(response, reverse('league:apply_success', args=[application.pk]))
        self.assertEqual(application.city, 'Ульяновск')

    def test_application_requires_consent(self):
        response = self.client.post(reverse('league:apply'), {
            'tournament': self.tournament.pk,
            'team': 'Без согласия',
            'captain': 'Иванов Иван',
            'players_count': 5,
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Application.objects.filter(team='Без согласия').exists())


class AccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='player@mail.ru',
            email='player@mail.ru',
            password='secret12345',
        )
        self.staff = User.objects.create_user(
            username='staff@mail.ru',
            email='staff@mail.ru',
            password='secret12345',
            is_staff=True,
        )

    def test_login_by_email(self):
        response = self.client.post(reverse('league:login'), {
            'email': 'player@mail.ru',
            'password': 'secret12345',
        })
        self.assertRedirects(response, reverse('league:account'))

    def test_account_requires_login(self):
        response = self.client.get(reverse('league:account'))
        self.assertRedirects(
            response,
            f"{reverse('league:login')}?next={reverse('league:account')}",
        )

    def test_panel_requires_staff(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('league:panel'))
        self.assertRedirects(
            response,
            f"{reverse('league:login')}?next={reverse('league:panel')}",
        )

    def test_staff_can_approve_application(self):
        self.client.force_login(self.staff)
        application = Application.objects.filter(status='pending').first()
        response = self.client.post(reverse('league:panel'), {
            'action': 'approve',
            'application': application.pk,
        })
        self.assertRedirects(response, reverse('league:panel'))
        application.refresh_from_db()
        self.assertEqual(application.status, 'approved')
