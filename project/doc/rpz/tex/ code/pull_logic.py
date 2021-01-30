from ..models import PullPlayers
from .user import UsersLogic

from ..repository import UsersCRUD

class PullPlayersLogic:

    def __init__(self):
        self.objects = PullPlayers.objects
        self.users_logic = UsersLogic()
        self.users_manager = UsersCRUD()


    def user_is_admin(self, user):
        return self.users_logic.user_is_admin(user)

    def user_in_pull(self, user_pk):
        users = self.users_manager.get_note_by_user_pk(user_pk)
        return self.objects.is_user_exists(users.pk)

    def user_in_pull2(self, users_pk):
        return self.objects.is_user_exists(users_pk)
