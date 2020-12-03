from ..models import Users, Games, PullPlayers, Friends


class UsersCRUD:
    def __init__(self):
        self.objects = Users.objects

    def get_all(self):
        return self.objects.get_all()

    def get_note(self, users_pk):
        return self.objects.get_note(users_pk)

    def get_note_by_user_pk(self, user_pk):
        return self.objects.get_note_by_user_pk(user_pk)

    def create_note(self, validated_data):
        return self.objects.create_note(validated_data)

    def update_note(self, validated_data, pk):
        return self.objects.update_note(validated_data, pk)


class FriendsCRUD:
    def __init__(self):
        self.objects = Friends.objects
        self.user_objects = Users.objects

    def get_all(self, user_pk, reverse):
        users = self.user_objects.get_note_by_user_pk(user_pk)
        return self.objects.get_all(users.pk, reverse)

    def get_note(self, friend_pk, user_pk, reverse):
        users = self.user_objects.get_note_by_user_pk(user_pk)
        return self.objects.get_note(friend_pk, users.pk, reverse)

    def delete_note(self, friend_pk, user_pk):
        users = self.user_objects.get_note_by_user_pk(user_pk)
        self.objects.delete_note(friend_pk, users.pk)

    def create_note(self, friend_pk, user_pk):
        users = self.user_objects.get_note_by_user_pk(user_pk)
        return self.objects.create_note(friend_pk, users.pk, self.user_objects)

    def update_note(self, friend_pk, user_pk, ready_to_play):
        users = self.user_objects.get_note_by_user_pk(user_pk)
        return self.objects.update_note(friend_pk, users.pk, ready_to_play)


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

    def create_note(self, user_pk):
        users = self.user_objects.get_note_by_user_pk(user_pk)
        return self.objects.create_note(self.user_objects.get_note(users.pk))


class GamesCRUD:

    def __init__(self):
        self.objects = Games.objects
        self.user_objects = Users.objects

    def get_all(self):
        return self.objects.get_all()

    def get_active_notes(self):
        return self.objects.get_notes(status='-1')

    def create_note(self, validated_data):
        friend = self.user_objects.get_note(validated_data['player_1_id'])
        user = self.user_objects.get_note(validated_data['player_2_id'])
        return self.objects.create_note(validated_data, user, friend)

    def get_note(self, game_id):
        return self.objects.get_note(game_id)

    def delete_note(self, game_id):
        return self.objects.delete_note(game_id)

    def update_note(self, validated_data, game_id):
        return self.objects.update_note(validated_data, game_id)

    def update_user_note(self, data, game_id):
        data.pop('player_1')
        data.pop('player_2')
        data.pop('date_time_from')
        return self.objects.update_note(data, game_id)
