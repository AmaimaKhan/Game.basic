from django.db import models
from django.utils import timezone

class Score(models.Model):
    player_name = models.CharField(max_length=50)
    score = models.IntegerField()
    date_played = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.player_name} - {self.score}"

