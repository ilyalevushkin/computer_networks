from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from ..repository import PullPlayersCRUD
from ..serializers import PullPlayersSerializer
from ..business_logic import PullPlayersLogic


class PullPlayersView(APIView):
    manager = PullPlayersCRUD()
    logic = PullPlayersLogic()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    #permission_classes = [permissions.AllowAny]

    # получает всех пользователей
    def get(self, request):
        query_set = self.manager.get_all()
        serializer = PullPlayersSerializer(query_set, many=True)
        json_data = serializer.data

        return Response({'Pull_players': json_data}, status=status.HTTP_200_OK)

    # добавить себя в пул
    def post(self, request):
        if not self.logic.user_in_pull(request.user.pk):
            self.manager.create_note(request.user.pk)
        else:
            return Response(f'User is already in pull', status=status.HTTP_403_FORBIDDEN)

        return Response({"success": f'User was added in pull successfully'},
                        status=status.HTTP_201_CREATED)

    def delete(self, request):
        if self.logic.user_in_pull(request.user.pk):
            self.manager.delete_note(request.user.pk)
        else:
            return Response(f'User is not in pull', status=status.HTTP_403_FORBIDDEN)

        return Response({"success": f'User was deleted from pull successfully'},
                        status=status.HTTP_200_OK)

