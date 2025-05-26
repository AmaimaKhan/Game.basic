from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

class GameRoom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    players = models.ManyToManyField(User, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Score(models.Model):
    player_name = models.CharField(max_length=50)
    score = models.IntegerField()
    date_played = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.player_name} - {self.score}"

