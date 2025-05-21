from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('play/', views.play, name='play'),
    path('play-again/', views.play_again, name='play_again'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
