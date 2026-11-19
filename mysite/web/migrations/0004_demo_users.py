from django.contrib.auth.hashers import make_password
from django.db import migrations

DEMO_USERS = [
    {
        'username': 'captain@mail.ru',
        'email': 'captain@mail.ru',
        'password': 'password',
        'first_name': 'Никита',
        'last_name': 'Маняков',
        'is_staff': False,
        'is_superuser': False,
    },
    {
        'username': 'admin@foot73.ru',
        'email': 'admin@foot73.ru',
        'password': 'admin12345',
        'first_name': 'Организатор',
        'last_name': 'Лиги',
        'is_staff': True,
        'is_superuser': True,
    },
]


def create_demo_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    for data in DEMO_USERS:
        values = dict(data)
        password = values.pop('password')
        user, created = User.objects.get_or_create(
            username=values['username'],
            defaults=values,
        )
        if created:
            user.password = make_password(password)
            user.save(update_fields=['password'])


def remove_demo_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username__in=[data['username'] for data in DEMO_USERS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('web', '0003_tournament_slug_application_city'),
    ]

    operations = [
        migrations.RunPython(create_demo_users, remove_demo_users),
    ]
