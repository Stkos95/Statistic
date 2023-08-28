from django.urls import path
from . import views


urlpatterns = [
    # path('test/', views.TestDate.as_view(), name='test'),
    # path('test1/', views.Test.as_view(), name='test'),
    path('schedule/<int:task_id>/', views.task_detail, name='task_detail'),
    path('schedule/', views.schedule_redirect, name='schedule'),
    # path('schedule/<slug:category_slug>/', views.schedule, name='schedule_category'),
    path('schedule/<slug>/', views.Test.as_view(), name='schedule_category'),
    path('schedule/<slug:category_slug>/create/', views.create_task, name='task_create'),
    path('schedule/<slug:slug>/<date>/', views.Test.as_view(), name='schedule_time'),

    path('about/', views.about, name='about'),

]