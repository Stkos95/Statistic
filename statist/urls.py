from django.urls import path
from . import views



app_name = 'statistic'

urlpatterns = [

    path('', views.InitView.as_view(), name='initial'),
    path('pl/', views.CountStatisticView.as_view(), name='count'),
    path('pl/<game_id>/', views.CountStatisticView.as_view(), name='count_existed'),

    path('game-result/<int:game_id>/', views.ResultStatisticView.as_view(), name='result'),
    path('game-result/<int:game_id>/<int:player_id>', views.ResultStatisticView.as_view(), name='result_player'),

    path('initial/', views.initial_players, name='initial_players'),
    path('count/', views.count_statistic, name='count_process'),
    path('player/', views.get_player_data, name='player_data'),
    path('close/', views.on_close, name='on_close'),

    path('check-players/', views.get_prepopulated_players, name='get_players'),


    # path('settings/create_type/', views.CreateGameType.as_view(), name='create_game_type') # endpoint to create custom game type.



]

