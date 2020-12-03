from django.db import models


class FriendManager(models.Manager):

    def get_all(self, users_pk, reverse):
        if not reverse:
            return self.filter(user_friend__pk=users_pk)
        else:
            return self.filter(friend__pk=users_pk)

    def create_note(self, friend_pk, users_pk, user_objects):
        user = user_objects.get(pk=users_pk)
        friend = user_objects.get(pk=friend_pk)
        friendship = self.create(user_friend=user, friend=friend)
        friendship.save()
        return friendship

    def get_note(self, friend_pk, users_pk, reverse):
        if not reverse:
            return self.filter(user_friend__pk=users_pk).get(friend__pk=friend_pk)
        else:
            return self.filter(friend__pk=users_pk).get(user_friend__pk=friend_pk)

    def delete_note(self, friend_pk, users_pk):
        friendship = self.filter(user_friend__pk=users_pk).get(friend__pk=friend_pk)
        friendship.delete()

    def update_note(self, friend_pk, users_pk, ready_to_play):
        friendship = self.filter(user_friend__pk=users_pk).get(friend__pk=friend_pk)
        if ready_to_play:
            friendship.status = 'Да'
        else:
            friendship.status = 'Нет'
        friendship.save()
        return friendship

    def is_friend_ready(self, friend_pk, users_pk):
        friendship = self.filter(user_friend__pk=friend_pk).get(friend__pk=users_pk)
        if friendship.status == 'Да':
            return True
        else:
            return False

    def is_friend_exists(self, friend_pk, users_pk):
        return self.filter(user_friend__pk=users_pk).filter(friend__pk=friend_pk).exists()
