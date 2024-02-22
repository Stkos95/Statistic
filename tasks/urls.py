from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'tasks'

urlpatterns = [
    path('', views.home, name='home'),
    path('schedule/', views.schedule_redirect, name='schedule'),
    path('schedule/<int:pk>/', views.TaskDetail.as_view(), name='task_detail'),
    path('schedule/<slug>/', views.Test.as_view(), name='schedule_category'),
    path('schedule/<slug:slug>/create/', views.CreateTask.as_view(), name='task_create'),
    path('schedule/<slug:slug>/<date>/', views.Test.as_view(), name='schedule_time'),

    path('about/', views.about, name='about'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),

]