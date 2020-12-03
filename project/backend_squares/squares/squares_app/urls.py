from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import UsersView, UsersSignInView, UsersSignOutView, UsersSignUpView, UserView
from .views import FriendsView, FriendView
from .views import PullPlayersView
from .views import GamesView, GameView

schema_view = get_schema_view(
   openapi.Info(
      title="Squares API",
      default_version='v1',
      description="API Specification",
      terms_of_service="http://localhost:8000/api/v1",
      contact=openapi.Contact(email="ilyalyov@mail.ru"),
      #license=openapi.License(name="BSD License"),
   ),
   public=True,
   #permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-token-auth', views.obtain_jwt_token),
    path('api-token-refresh', views.refresh_jwt_token),
    path('users', UsersView.as_view()),
    path('users/signup', UsersSignUpView.as_view()),
    path('users/signin', UsersSignInView.as_view()),
    path('users/signout', UsersSignOutView.as_view()),
    path('users/<int:pk>', UserView.as_view()),
    path('friends', FriendsView.as_view()),
    path('friends/<int:pk>', FriendView.as_view()),
    path('pull_players', PullPlayersView.as_view()),
    path('games', GamesView.as_view()),
    path('games/<int:pk>', GameView.as_view()),
]
