from django import forms

from .models import Application, Tournament


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['title', 'format', 'start_date', 'end_date', 'team_limit', 'fee', 'venue']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Например, Кубок весны 2027'}),
            'format': forms.Select(attrs={'class': 'select'}),
            'start_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'team_limit': forms.NumberInput(attrs={'class': 'input', 'min': 2, 'max': 64}),
            'fee': forms.NumberInput(attrs={'class': 'input', 'min': 0}),
            'venue': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Спортзал УлГТУ'}),
        }
        labels = {
            'title': 'Название',
            'format': 'Формат',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
            'team_limit': 'Лимит команд',
            'fee': 'Взнос, ₽',
            'venue': 'Площадка',
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')
        if start and end and end <= start:
            self.add_error('end_date', 'Дата окончания должна быть позже начала')
        return cleaned


class ApplicationForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        label='Согласен на обработку персональных данных',
        error_messages={'required': 'Подтвердите согласие на обработку персональных данных.'},
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = Application
        fields = ['tournament', 'team', 'city', 'captain', 'phone', 'email', 'players_count', 'comment']
        widgets = {
            'tournament': forms.Select(attrs={'class': 'select'}),
            'team': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Например, Волга'}),
            'city': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Ульяновск'}),
            'captain': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Фамилия Имя Отчество'}),
            'phone': forms.TextInput(attrs={'class': 'input', 'type': 'tel', 'placeholder': '+7 900 000-00-00'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'captain@mail.ru'}),
            'players_count': forms.NumberInput(attrs={'class': 'input', 'min': 5, 'max': 12}),
            'comment': forms.Textarea(attrs={
                'class': 'textarea',
                'rows': 3,
                'placeholder': 'Например: нужен перенос матча 1-го тура',
            }),
        }
        labels = {
            'tournament': 'Турнир',
            'team': 'Название команды',
            'city': 'Город',
            'captain': 'Капитан: ФИО',
            'phone': 'Телефон',
            'email': 'E-mail',
            'players_count': 'Игроков в составе',
            'comment': 'Комментарий организатору',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tournament'].queryset = Tournament.objects.filter(status='published')
        self.fields['tournament'].empty_label = 'Выберите турнир'
