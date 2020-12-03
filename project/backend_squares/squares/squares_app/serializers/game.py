from rest_framework import serializers

from .user import UsersSerializer


class GameStatesSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=2)
    turn = serializers.CharField(max_length=1)
    player_1_points = serializers.IntegerField()
    player_2_points = serializers.IntegerField()

    columns = serializers.IntegerField()
    rows = serializers.IntegerField()
    table_with_chips = serializers.CharField(max_length=10000)


class GameStatesUpdateSerializer(serializers.Serializer):
    column_pos = serializers.IntegerField(min_value=0)
    row_pos = serializers.IntegerField(min_value=0)
    value = serializers.CharField(max_length=1)


class GamesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    player_1_id = serializers.IntegerField()
    player_2_id = serializers.IntegerField()
    game_state = GameStatesSerializer()

    date_time_from = serializers.DateTimeField(required=False)
    date_time_to = serializers.DateTimeField(required=False)


class GamesResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    player_1 = UsersSerializer()
    player_2 = UsersSerializer()
    game_state = GameStatesSerializer()

    date_time_from = serializers.DateTimeField()
    date_time_to = serializers.DateTimeField()
