from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.contrib.auth.hashers import check_password

class UsersManager(models.Manager):
    def get_all(self):
        return self.order_by('user')

    def create_note(self, data):
        user = User.objects.create(**data['user'])
        data.pop('user')
        data.update({'user_id': user.id})
        return self.create(**data)

    def get_note(self, pk):
        return self.get(pk=pk)

    def get_note_by_user_pk(self, pk):
        return self.get(user__pk=pk)

    def update_note(self, data, users_pk):
        user_info = self.get(pk=users_pk)
        if data.get('user', False):
            user = User.objects.get(pk=user_info.user.pk)
            self.update_elem_by_dict(user, data['user'])
            data.pop('user')

        self.update_elem_by_dict(user_info, data)
        return self.get(pk=users_pk)

    def update_elem_by_dict(self, elem, d):
        for key, value in d.items():
            setattr(elem, key, value)
        elem.save()

    def is_user_exists(self, username):
        return not self.filter(user__username=username).exists()

    def is_user_correct_password(self, username, password):
        user = User.objects.filter(username=username)
        if user.exists():
            if user[0].is_staff:
                return check_password(password, user[0].password)
            else:
                return password == user[0].password

    def create_token_for_user(self, username, password):
        #if User.objects.get(username=username, password=password).exists():
        #    return False
        user = User.objects.get(username=username)
        all_user = self.get(user=user)
        if Token.objects.filter(user=user).exists():
            return False
        return Token.objects.create(user=user), all_user.pk

    def delete_token(self, token):
        token.delete()

    def is_staff(self, user):
        return user.is_staff

    def get_users_pk(self, user):
        return self.get(user__pk=user.pk)

