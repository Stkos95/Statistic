from django.contrib import admin
from .models import Actions

@admin.register(Actions)
class PlayersAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'slug']
    prepopulated_fields = {'slug': ('name',)}

