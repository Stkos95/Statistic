from django.urls import path
from . import views




urlpatterns = [
    path('schedule/<int:task_id>/', views.task_detail, name='task_detail'),
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/category/<slug:category_slug>/', views.schedule, name='schedule_category'),
    path('schedule/<date>/<slug:category_slug>/', views.schedule, name='schedule_category_time'),
    path('schedule/<date>/', views.schedule, name='schedule_time'),
    path('about/', views.about, name='about'),


]