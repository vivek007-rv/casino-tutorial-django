from django.contrib import admin
from .models import GameSession, Transaction

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'result', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'result')
    ordering = ('-timestamp',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'transaction_date')
    list_filter = ('status', 'transaction_date', 'user')
    search_fields = ('user__username',)
    ordering = ('-transaction_date',)
