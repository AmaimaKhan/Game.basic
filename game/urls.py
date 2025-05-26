from django.urls import path
from . import views, api_views

urlpatterns = [
    path('', views.index, name='index'),
    path('play/', views.play, name='play'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('game-over/', views.game_over, name='game_over'),
    path('api/start/', api_views.start_game),
    path('api/guess/', api_views.guess_card),
]
