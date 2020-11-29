from django.db import models

from .users import Users

class PullPlayers(models.Model):
    player = models.ForeignKey(Users, on_delete=models.PROTECT)