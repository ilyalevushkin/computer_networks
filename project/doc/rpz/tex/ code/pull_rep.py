from ..models import Users, Games, PullPlayers, Friends


class PullPlayersCRUD:

    def __init__(self):
        self.objects = PullPlayers.objects
        self.user_objects = Users.objects

    def get_all(self):
        return self.objects.get_all()

    def get_note(self, user_pk):
        users = self.user_objects.get_note_by_user_pk(user_pk)
        return self.objects.get_note(users.pk)

    def delete_note(self, user_pk):
        users = self.user_objects.get_note_by_user_pk(user_pk)
        self.objects.delete_note(self.user_objects.get_note(users.pk))

    def delete_note2(self, users_pk):
        self.objects.delete_note(self.user_objects.get_note(users_pk))

    def create_note(self, user_pk):
        users = self.user_objects.get_note_by_user_pk(user_pk)
        return self.objects.create_note(self.user_objects.get_note(users.pk))

