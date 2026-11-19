from django.db import migrations, models
from django.utils.text import slugify

CYRILLIC_TO_LATIN = str.maketrans({
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
})


def make_slug(value):
    return slugify(value.lower().translate(CYRILLIC_TO_LATIN))


def fill_slugs(apps, schema_editor):
    Tournament = apps.get_model('web', 'Tournament')
    used = set()
    for tournament in Tournament.objects.all().order_by('pk'):
        base = make_slug(tournament.title) or f'tournament-{tournament.pk}'
        slug = base
        number = 2
        while slug in used:
            slug = f'{base}-{number}'
            number += 1
        used.add(slug)
        tournament.slug = slug
        tournament.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_seed_demo'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=140),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application',
            name='city',
            field=models.CharField(blank=True, max_length=80, verbose_name='Город'),
        ),
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='tournament',
            name='slug',
            field=models.SlugField(blank=True, max_length=140, unique=True, verbose_name='Слаг'),
        ),
    ]
