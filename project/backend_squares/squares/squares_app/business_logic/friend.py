from ..models import Users, Friends


class FriendsLogic:

    def __init__(self):
        self.objects = Friends.objects
        self.user_objects = Users.objects

    def user_exists(self, users_pk):
        return self.user_objects.is_user_exists(users_pk)

    def friend_exists(self, friend_pk, user_pk):
        users = self.user_objects.get_note_by_user_pk(user_pk)
        return self.objects.is_friend_exists(friend_pk, users.pk)

    def is_reverse(self, reverse):
        return reverse

    def is_ready(self, ready):
        return ready

    def friend_ready(self, friend_pk, users_pk):
        return self.objects.is_friend_ready(friend_pk, users_pk)

