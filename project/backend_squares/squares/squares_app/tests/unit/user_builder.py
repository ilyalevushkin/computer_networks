from ...models.users import Users

class UserBuilder:
    def __init__(self, username, password):
        self.user = Users.objects.create_note({'user': {'username': username, 'password': password}})

    def with_photo(self, photo):
        self.user.photo = photo
        return self

    def with_phone(self, phone):
        self.user.phone = phone
        return self

    def with_about(self, about):
        self.user.about = about
        return self

    def with_first_name(self, first_name):
        self.user.user.first_name = first_name
        return self

    def with_first_name(self, first_name):
        self.user.user.first_name = first_name
        return self

    def with_last_name(self, last_name):
        self.user.user.last_name = last_name
        return self

    def with_email(self, email):
        self.user.user.email = email
        return self

    def build(self):
        return self.user
