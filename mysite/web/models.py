from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

CYRILLIC_TO_LATIN = str.maketrans({
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
})


def make_slug(value):
    """Return an ASCII slug that also works for Russian titles."""
    return slugify(value.lower().translate(CYRILLIC_TO_LATIN))


class Tournament(models.Model):
    FORMAT_CHOICES = [
        ('5x5', '5×5'),
        ('8x8', '8×8'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
    ]

    title = models.CharField('Название', max_length=120)
    slug = models.SlugField('Слаг', max_length=140, unique=True, blank=True)
    format = models.CharField('Формат', max_length=8, choices=FORMAT_CHOICES, default='5x5')
    start_date = models.DateField('Дата начала')
    end_date = models.DateField('Дата окончания')
    team_limit = models.PositiveIntegerField('Лимит команд', default=12)
    fee = models.PositiveIntegerField('Взнос, ₽', default=6000)
    venue = models.CharField('Площадка', max_length=120, blank=True)
    status = models.CharField('Статус', max_length=12, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'
        ordering = ['start_date', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = make_slug(self.title) or f'tournament-{uuid4().hex[:8]}'
            slug = base
            number = 2
            while Tournament.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{number}'
                number += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('league:tournament_detail', args=[self.slug])


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На проверке'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
        ('draft', 'Черновик'),
    ]

    team = models.CharField('Команда', max_length=80)
    tournament = models.ForeignKey(
        Tournament,
        verbose_name='Турнир',
        on_delete=models.CASCADE,
        related_name='applications',
    )
    captain = models.CharField('Капитан', max_length=120)
    city = models.CharField('Город', max_length=80, blank=True)
    phone = models.CharField('Телефон', max_length=24, blank=True)
    email = models.EmailField('E-mail', blank=True)
    players_count = models.PositiveSmallIntegerField('Игроков в составе', default=5)
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField('Статус', max_length=12, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Подана', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.team} — {self.tournament}'
