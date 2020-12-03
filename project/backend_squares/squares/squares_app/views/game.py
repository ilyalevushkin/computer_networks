from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from ..repository import GamesCRUD
from ..serializers import GamesSerializer, GamesResponseSerializer, GameStatesUpdateSerializer
from ..business_logic import GamesLogic

class GamesView(APIView):
    manager = GamesCRUD()
    logic = GamesLogic()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # возвращает все игры
    def get(self, request):
        if self.logic.user_is_admin(request.user):
            if self.logic.is_active(request.GET.get('active', False)):
                query_set = self.manager.get_active_notes()
            else:
                query_set = self.manager.get_all()

            serializer = GamesSerializer(query_set, many=True)
            json_data = serializer.data

            return Response({'Games': json_data})
        else:
            return Response('User has no rights for this operation', status=status.HTTP_403_FORBIDDEN)


    # создает игру
    def post(self, request):
        json_data = request.data.get('Game')

        serializer = GamesSerializer(data=json_data)
        if serializer.is_valid(raise_exception=True):
            serializer.is_valid()
            validated_data = serializer.validated_data
            if self.logic.is_user_valid(validated_data['player_1_id'], request.user.pk,
                                        validated_data['player_2_id']):
                game = self.manager.create_note(validated_data)

                serializer = GamesResponseSerializer(game, many=False)
                json_data = serializer.data

                return Response({'Game': json_data}, status=status.HTTP_200_OK)
            else:
                return Response('One of User\'s does not exist or opponent not ready to play',
                                status=status.HTTP_403_FORBIDDEN)



class GameView(APIView):
    manager = GamesCRUD()
    logic = GamesLogic()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # получает информацию о конкретной игре
    def get(self, request, pk):
        if not self.logic.game_exists(pk):
            return Response('Game does not exist', status=status.HTTP_404_NOT_FOUND)
        elif self.logic.user_is_admin(request.user) or self.logic.game_is_users(request.user, pk):
            query_set = self.manager.get_note(pk)

            serializer = GamesResponseSerializer(query_set, many=False)
            json_data = serializer.data

            return Response({'Game': json_data})
        else:
            return Response('User has no rights for this operation', status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, pk):
        if not self.logic.game_exists(pk):
            return Response('Game does not exist', status=status.HTTP_404_NOT_FOUND)

        if self.logic.game_is_users(request.user, pk):
            json_data = request.data.get('Game_state_update')

            serializer = GameStatesUpdateSerializer(data=json_data)
            if serializer.is_valid(raise_exception=True):
                serializer.is_valid()
                validated_data = serializer.validated_data
                # проверяем, правильно ли обновляет игру пользователь (делает ход)
                if self.logic.update_game_is_correct(request.user, pk, validated_data):
                    # обновляем игру на основе сделанного пользователем хода
                    calculated_data = self.logic.make_turn(pk, validated_data)

                    serializer = GamesResponseSerializer(calculated_data, many=False)
                    game = self.manager.update_user_note(serializer.data, pk)

                    serializer = GamesResponseSerializer(game, many=False)
                    json_data = serializer.data

                    return Response({'Game': json_data}, status=status.HTTP_200_OK)
                else:
                    return Response('User cheats', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('User has no rights for this operation', status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        if not self.logic.game_exists(pk):
            return Response('Game does not exist', status=status.HTTP_404_NOT_FOUND)
        elif self.logic.user_is_admin(request.user):
            self.manager.delete_note(pk)

            return Response({"success": f"Game {pk} was deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response('User has no rights for this operation', status=status.HTTP_403_FORBIDDEN)
