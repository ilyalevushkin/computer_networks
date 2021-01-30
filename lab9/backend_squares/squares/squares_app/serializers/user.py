from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=200, required=False)
    last_name = serializers.CharField(max_length=200, required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=200, write_only=True)


class UsersSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer()
    phone = serializers.CharField(max_length=30, required=False)
    about = serializers.CharField(max_length=1000, required=False)
    photo = serializers.CharField(max_length=200, required=False)


class UsersSignInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200, write_only=True)



class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=False, allow_blank=True)
    first_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(max_length=200, write_only=True, required=False)


class UsersUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    user = UserUpdateSerializer(required=False)
    phone = serializers.CharField(max_length=30, required=False, allow_blank=True)
    about = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    photo = serializers.CharField(max_length=200, required=False, allow_blank=True)


