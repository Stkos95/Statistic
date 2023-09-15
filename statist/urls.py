from django.urls import path
from . import views



app_name = 'statistic'

urlpatterns = [
    # path('', views.PlayersView.as_view(), name='home'),
    path('', views.CountStatisticView.as_view(), name='count'),
    path('result/', views.ResultStatisticView.as_view(), name='result'),
    path('test/', views.ajax_action, name='ajax')
]