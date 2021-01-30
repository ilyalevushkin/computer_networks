from rest_framework import serializers

from .user import UsersSerializer

class FriendsSerializer(serializers.Serializer):
    id = serializers.IntegerField(write_only=True)
    user_friend = UsersSerializer(read_only=True)
    friend = UsersSerializer(read_only=True)
    status = serializers.CharField(max_length=3, required=False)

class FriendsUpdateSerializer(serializers.Serializer):
    ready_to_play = serializers.BooleanField()
