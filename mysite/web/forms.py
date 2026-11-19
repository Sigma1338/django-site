from django import forms

from .models import Tournament


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
