from django.urls import path
from . import views



app_name = 'statistic'

urlpatterns = [
    path('', views.PlayersView.as_view(), name='home'),
    path('count/', views.CountStatistic.as_view(), name='count')
]