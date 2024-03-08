from django.urls import path
from . import views


app_name = 'settings'

urlpatterns = [
    path('', views.SettingsListView.as_view(), name='settings'),
    path('statistic/', views.SettingsStatistic.as_view(), name='settings_statistic'),
    path('statistic/manage-types/', views.TypesManageView.as_view(), name='manage_types'),
    path('statistic/manage-types/create', views.TypesDetailView.as_view(), name='create_type'),
    path('statistic/manage-types/<id>/<slug>/', views.TypesDetailView.as_view(), name='detail_type'),

    path('statistic/manage-teams/', views.TeamsManageView.as_view(), name='manage_teams'),
    path('statistic/manage-team/create/', views.TeamDetailView.as_view(), name='create_team'),
    path('statistic/manage-teams/<int:pk>/', views.TeamDetailView.as_view(), name='detail_team'),


]


