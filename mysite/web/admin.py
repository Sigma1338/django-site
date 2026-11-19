from django.contrib import admin

from .models import Application, Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('title', 'format', 'start_date', 'end_date', 'team_limit', 'fee', 'status')
    list_filter = ('format', 'status')
    search_fields = ('title', 'venue')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('team', 'tournament', 'captain', 'players_count', 'status', 'created_at')
    list_filter = ('status', 'tournament')
    search_fields = ('team', 'captain', 'email')
    actions = ('approve', 'reject')

    @admin.action(description='Одобрить выбранные заявки')
    def approve(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'Одобрено заявок: {updated}')

    @admin.action(description='Отклонить выбранные заявки')
    def reject(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'Отклонено заявок: {updated}')
