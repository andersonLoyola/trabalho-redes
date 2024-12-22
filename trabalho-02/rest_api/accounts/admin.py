from django.contrib import admin
from .models import AccountsConnection

@admin.register(AccountsConnection)
class AccountsConnectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'connection_id', 'created_at')
