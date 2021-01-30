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

    # добавить себя в пул
    def post(self, request):
        if not self.logic.user_in_pull(request.user.pk):
            self.manager.create_note(request.user.pk)
        else:
            return Response(f'User is already in pull', status=status.HTTP_403_FORBIDDEN)

        return Response({"success": f'User was added in pull successfully'},
                        status=status.HTTP_201_CREATED)

