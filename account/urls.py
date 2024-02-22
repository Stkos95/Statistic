from django.urls import path, include
from django.contrib.auth import urls
from . import views
from django.contrib.auth import views as auth_views


# app_name = 'account'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')) Убрал, чтобы реализовать самому

    # path('login/', views.login_view, name='login')
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('registration/', views.registration_view, name='registration'),
    path('password-change/', views.change_password_view, name='password_change'),
    # path('password-change/', auth_views.PasswordChangeView.as_view(), name='password-change')

    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')



]