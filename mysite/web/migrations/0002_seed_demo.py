from datetime import date

from django.db import migrations


def seed_demo_data(apps, schema_editor):
    Tournament = apps.get_model('web', 'Tournament')
    Application = apps.get_model('web', 'Application')

    cup, _ = Tournament.objects.get_or_create(
        title='Кубок Ульяновска по мини-футболу',
        defaults={
            'format': '5x5',
            'start_date': date(2026, 11, 12),
            'end_date': date(2026, 12, 20),
            'team_limit': 16,
            'fee': 4500,
            'venue': 'Манеж «Спартак»',
            'status': 'published',
        },
    )
    winter, _ = Tournament.objects.get_or_create(
        title='Зимняя лига 2027',
        defaults={
            'format': '5x5',
            'start_date': date(2027, 1, 10),
            'end_date': date(2027, 2, 28),
            'team_limit': 12,
            'fee': 6000,
            'venue': 'ФОК «Олимпиец»',
            'status': 'published',
        },
    )
    weekend, _ = Tournament.objects.get_or_create(
        title='Турнир выходного дня',
        defaults={
            'format': '8x8',
            'start_date': date(2026, 11, 23),
            'end_date': date(2027, 2, 15),
            'team_limit': 12,
            'fee': 3000,
            'venue': 'Площадка «Северный Венец»',
            'status': 'published',
        },
    )

    demo_applications = [
        {
            'team': 'Волга',
            'tournament': cup,
            'captain': 'Маняков Н.',
            'phone': '+7 900 000-00-01',
            'email': 'volga@mail.ru',
            'players_count': 8,
            'status': 'pending',
        },
        {
            'team': 'Зенит',
            'tournament': cup,
            'captain': 'Кузнецов П.',
            'phone': '+7 900 000-00-02',
            'email': 'zenit@mail.ru',
            'players_count': 10,
            'status': 'approved',
        },
        {
            'team': 'Спартак',
            'tournament': winter,
            'captain': 'Иванов Д.',
            'phone': '+7 900 000-00-03',
            'email': 'spartak@mail.ru',
            'players_count': 9,
            'status': 'rejected',
        },
        {
            'team': 'Динамо',
            'tournament': weekend,
            'captain': 'Сидоров А.',
            'phone': '+7 900 000-00-04',
            'email': 'dinamo@mail.ru',
            'players_count': 11,
            'status': 'draft',
        },
        {
            'team': 'Торпедо',
            'tournament': winter,
            'captain': 'Абдуллин Р.',
            'phone': '+7 900 000-00-05',
            'email': 'torpedo@mail.ru',
            'players_count': 8,
            'status': 'pending',
        },
        {
            'team': 'Симбирск',
            'tournament': cup,
            'captain': 'Белов А.',
            'phone': '+7 900 000-00-06',
            'email': 'simbirsk@mail.ru',
            'players_count': 12,
            'status': 'approved',
        },
    ]

    for item in demo_applications:
        Application.objects.get_or_create(
            team=item['team'],
            tournament=item['tournament'],
            defaults=item,
        )


def unseed_demo_data(apps, schema_editor):
    Application = apps.get_model('web', 'Application')
    Tournament = apps.get_model('web', 'Tournament')
    Application.objects.all().delete()
    Tournament.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_demo_data, unseed_demo_data),
    ]
