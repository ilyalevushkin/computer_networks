from django.db import models



class PullPlayersManager(models.Manager):

    def get_all(self):
        return self.order_by('date_time_appear')

    def get_note(self, user):
        return self.get(player=user)

    def create_note(self, user):
        self.create(player=user)

    def delete_note(self, user):
        note = self.get_note(user)
        note.delete()

    def is_user_exists(self, users_pk):
        return self.filter(player__pk=users_pk).exists()
