from django.db import models
from .users import Users
from ..managers import PullPlayersManager

from datetime import datetime


class PullPlayers(models.Model):
    player = models.OneToOneField(Users, on_delete=models.PROTECT)

    date_time_appear = models.DateTimeField(default=datetime.now)

    objects = PullPlayersManager()

    def __str__(self):
        return self.player.user.username
