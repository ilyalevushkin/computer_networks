from django.db import models

from .users import Users
from .game_states import GameStates

from django.core.exceptions import ValidationError



class Games(models.Model):
    player_1 = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='player_1')
    player_2 = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='player_2')
    game_state = models.OneToOneField(GameStates, on_delete=models.CASCADE)

    date_time_from = models.DateTimeField()
    date_time_to = models.DateTimeField()

    def clean(self):
        if self.date_time_from > self.date_time_to:
            raise ValidationError(f'date_from: {self.date_time_from} more than date_to: {self.date_time_to}')