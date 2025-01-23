from django.contrib import admin

# Register your models here.
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')  # Colonnes affichées dans la liste
    list_filter = ('time_created', 'user')           # Filtres disponibles
    search_fields = ('title', 'description') 