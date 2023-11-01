from django.contrib import admin
from .models import Task, Category

@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    list_display = ['name', 'description', 'deadline', 'done', 'created', 'user']
    list_display_links = ['name', 'deadline', 'done']
    filter = ['user']

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


