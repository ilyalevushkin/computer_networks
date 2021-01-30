from ..models import Users


class UsersLogic:

    def __init__(self):
        self.objects = Users.objects

    def users_signup_check(self, username):
        return self.objects.is_user_exists(username)

    def users_signin_check(self, dict_data):
        return self.objects.is_user_correct_password(dict_data['username'], dict_data['password'])

    def create_token(self, dict_data):
        return self.objects.create_token_for_user(dict_data['username'], dict_data['password'])

    def delete_token(self, token):
        self.objects.delete_token(token)

    def user_is_admin(self, user):
        return self.objects.is_staff(user)

    def pk_is_users(self, user, pk):
        return self.objects.get_users_pk(user).pk == pk
