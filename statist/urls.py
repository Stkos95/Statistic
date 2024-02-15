from django.urls import path
from . import views



app_name = 'statistic'

urlpatterns = [
    # path('', views.PlayersView.as_view(), name='home'),
    path('', views.InitView.as_view(), name='initial'),
    path('pl/', views.CountStatisticView.as_view(), name='count'),
    path('pl/<game_id>/', views.CountStatisticView.as_view(), name='count_existed'),
    path('result/<game_id>/', views.ResultStatisticView.as_view(), name='result'),
    path('initial/', views.initial_players, name='initial_players'),
    path('count/', views.count_statistic, name='count_process'),
    path('player/', views.get_player_data, name='player_data'),
    path('close/', views.on_close, name='on_close'),
    path('check_players/', views.get_prepopulated_players, name='get_players'),
    path('settings/manage_types/', views.TypesManageView.as_view(), name='manage_types'),

    path('settings/manage_types/create', views.TypesDetailView.as_view(), name='create_type'),
    path('settings/manage_types/<id>/<slug>/', views.TypesDetailView.as_view(), name='detail_type'),
    # path('settings/create_type/', views.CreateGameType.as_view(), name='create_game_type') # endpoint to create custom game type.

    path('settings/manage_types/order/', views.test_order, name='test_order'),

]

