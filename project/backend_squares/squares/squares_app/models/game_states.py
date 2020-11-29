from django.db import models
from django.core.exceptions import ValidationError

class GameStates(models.Model):
    status_choices = (
        ('-1', 'Игра идет'),
        ('0', 'Ничья'),
        ('1', 'Первый игрок'),
        ('2', 'Второй игрок')
    )

    turn_choices = (
        ('1', 'Первый игрок'),
        ('2', 'Второй игрок')
    )

    transmission_mechanism = models.CharField(max_length=2, choices=status_choices)
    turn = models.CharField(max_length=1, choices=turn_choices)
    player_1_points = models.PositiveIntegerField(default=0)
    player_2_points = models.PositiveIntegerField(default=0)

    columns = models.PositiveIntegerField(default=11)
    rows = models.PositiveIntegerField(default=11)
    table_with_chips = models.TextField(default='0'*11*11)
