from django.db import models
from django.core.exceptions import ValidationError

from .users import Users
from .game_states import GameStates
from ..managers import GamesManager

from datetime import datetime

class Games(models.Model):
    player_1 = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='player_1')
    player_2 = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='player_2')
    game_state = models.OneToOneField(GameStates, on_delete=models.CASCADE)

    date_time_from = models.DateTimeField(default=datetime.now, blank=True)
    date_time_to = models.DateTimeField(default=datetime.now, blank=True)

    objects = GamesManager()

    def __str__(self):
        return f'{self.pk}, {self.player_1.user.username}, {self.player_2.user.username}'
