from django.db import models


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
