from django.contrib import admin
from .models import Actions, Players

@admin.register(Actions)
class ActionsAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
    list_display = ['name']

