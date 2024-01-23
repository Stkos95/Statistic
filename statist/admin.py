from django.contrib import admin
from .models import Actions, Players, ResultsJson, Game, Type

@admin.register(Actions)
class ActionsAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ResultsJson)
class ResultsJsonAdming(admin.ModelAdmin):
    list_display = ('player', 'value')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'date']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'halfs', 'user']
