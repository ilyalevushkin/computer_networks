from django.db import models

from .users import Users
from ..managers import FriendManager


class Friends(models.Model):
    status_choices = (
        ('Да', 'Готов играть'),
        ('Нет', 'Не готов играть')
    )

    user_friend = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='user_friend')
    friend = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='friend')

    status = models.CharField(max_length=3, choices=status_choices, default='Нет')

    objects = FriendManager()

    def __str__(self):
        return self.user_friend.user.username, self.friend.user.username
