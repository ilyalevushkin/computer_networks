from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from ..repository import FriendsCRUD
from ..serializers import UsersSerializer, FriendsSerializer, FriendsUpdateSerializer
from ..business_logic import FriendsLogic



class FriendsView(APIView):
    manager = FriendsCRUD()
    logic = FriendsLogic()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # получить всех друзей (с кем Я дружу) или(reverse) КТО со мной дружит
    def get(self, request):
        if self.logic.is_reverse(request.GET.get('reverse', False)):
            query_set = self.manager.get_all(request.user.pk, reverse=True)
        else:
            # получить тех, КТО со мной дружит (кинул запрос на дружбу, подписался на меня)
            query_set = self.manager.get_all(request.user.pk, reverse=False)

        serializer = FriendsSerializer(query_set, many=True)
        json_data = serializer.data

        return Response({'Friends': json_data})

    # добавить друга (или сделать запрос на дружбу)
    def post(self, request):
        json_data = request.data.get('Friendship')

        serializer = FriendsSerializer(data=json_data)

        if serializer.is_valid(raise_exception=True):
            serializer.is_valid()
            validated_data = serializer.validated_data

            if not self.logic.user_exists(validated_data['id']):
                return Response(f'User {validated_data} does not exist', status=status.HTTP_404_NOT_FOUND)
            elif not self.logic.friend_exists(validated_data['id'], request.user.pk):
                friend = self.manager.create_note(validated_data['id'], request.user.pk)
                serializer = FriendsSerializer(friend)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(f'User {validated_data} is already friend', status=status.HTTP_200_OK)


class FriendView(APIView):
    manager = FriendsCRUD()
    logic = FriendsLogic()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # получить информацию о друге
    def get(self, request, pk):
        if not self.logic.user_exists(pk):
            return Response(f'User {pk} does not exist', status=200)
        elif self.logic.friend_exists(pk, request.user.pk):
            reverse = self.logic.is_reverse(request.GET.get('reverse', False))
            query_set = self.manager.get_note(pk, request.user.pk, reverse=reverse)

            serializer = FriendsSerializer(query_set, many=False)
            json_data = serializer.data

            return Response(json_data, status=status.HTTP_200_OK)

        else:
            return Response(f'User {pk} is not {request.user.pk}\'s friend', status=status.HTTP_200_OK)

    # удалить друга
    def delete(self, request, pk):
        if not self.logic.user_exists(pk):
            return Response(f'User was not found', status=status.HTTP_404_NOT_FOUND)
        elif self.logic.friend_exists(pk, request.user.pk):
            self.manager.delete_note(pk, request.user.pk)
            return Response({"success": f"Friend {pk} was deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response('Friend was not found', status=status.HTTP_404_NOT_FOUND)

    # обновить статус готовности к игре с другом
    def patch(self, request, pk):
        json_data = request.data.get('Status')

        serializer = FriendsUpdateSerializer(data=json_data)
        if serializer.is_valid(raise_exception=True):
            serializer.is_valid()
            validated_data = serializer.validated_data

            friendship = self.manager.update_note(pk, request.user.pk, validated_data['ready_to_play'])
            serializer = FriendsSerializer(friendship, many=False)
            json_data = serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
