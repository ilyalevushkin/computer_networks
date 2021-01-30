from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import json

from ..repository import UsersCRUD
from ..serializers import UsersSerializer, UsersSignInSerializer, UsersUpdateSerializer
from ..business_logic import UsersLogic



# получить всех пользователей
class UsersView(APIView):
    manager = UsersCRUD()
    logic = UsersLogic()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        query_set = self.manager.get_all()

        serializer = UsersSerializer(query_set, many=True)
        json_data = serializer.data

        return Response({'Users': json_data}, status=status.HTTP_200_OK)
        # business logic (можно ли делать такой запрос ему или нет)
        # достать данные из модели users (работа будет осуществляться в managers, паттерн repository, метод read
        # преобразование к DTO (осуществляется с помощью serializer)


# создание нового пользователя
class UsersSignUpView(APIView):

    manager = UsersCRUD()
    logic = UsersLogic()

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        json_data = request.data.get('User')

        serializer = UsersSerializer(data=json_data)
        username = 'no_user'
        if serializer.is_valid(raise_exception=True):
            serializer.is_valid()
            validated_data = serializer.validated_data
            username = validated_data['user']['username']

            if self.logic.users_signup_check(username):
                self.manager.create_note(validated_data)
            else:
                return Response(f'User {username} exists', status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "User '{}' created successfully".format(username)}, status=status.HTTP_201_CREATED)



# выход из аккаунта
class UsersSignOutView(APIView):
    manager = UsersCRUD()
    logic = UsersLogic()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        token = request.auth
        self.logic.delete_token(token)

        return Response("You were successfully logged out", status=status.HTTP_200_OK)


# вход в аккаунт
class UsersSignInView(APIView):

    manager = UsersCRUD()
    logic = UsersLogic()

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        json_data = request.data.get('User_signin')

        serializer = UsersSignInSerializer(data=json_data)

        token = 'no_token'
        user_pk = -1
        if serializer.is_valid(raise_exception=True):
            serializer.is_valid()
            validated_data = serializer.validated_data

            if self.logic.users_signin_check(validated_data):
                token, user_pk = self.logic.create_token(validated_data)
                if not token:
                    return Response('User has already logged in', status=status.HTTP_200_OK)
            else:
                return Response('User does not exist or wrong password', status=status.HTTP_400_BAD_REQUEST)

        return Response({'Token': str(token), 'id': user_pk}, status=status.HTTP_200_OK)



class UserView(APIView):

    manager = UsersCRUD()
    logic = UsersLogic()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # получить данные пользователя
    def get(self, request, pk):
        query_set = self.manager.get_note(pk)

        serializer = UsersSerializer(query_set, many=False)
        json_data = serializer.data

        return Response({'User': json_data}, status=status.HTTP_200_OK)

    # изменить данные пользователя
    def patch(self, request, pk):
        if self.logic.user_is_admin(request.user) or self.logic.pk_is_users(request.user, pk):
            json_data = request.data.get('User_update')

            serializer = UsersUpdateSerializer(data=json_data)
            print(json_data)
            if serializer.is_valid(raise_exception=True):
                serializer.is_valid()
                validated_data = serializer.validated_data
                res = self.manager.update_note(validated_data, pk)

                serializer = UsersSerializer(res, many=False)
                json_data = serializer.data

                return Response({"User_update": json_data}, status=status.HTTP_200_OK)
        else:
            return Response('User has no rights for this operation', status=status.HTTP_403_FORBIDDEN)
