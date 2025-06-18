from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.index, name='index'),
    path('game/', views.game_simulation, name='game_simulation'),
    path('deposit/', views.deposit, name='deposit'),
    path('history/', views.history, name='history'),
]
