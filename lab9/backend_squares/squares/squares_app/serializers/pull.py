from rest_framework import serializers

from .user import UsersSerializer


class PullPlayersSerializer(serializers.Serializer):
    player = UsersSerializer()
    date_time_appear = serializers.DateTimeField(read_only=True)
