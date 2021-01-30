from django.test import TestCase

from ...business_logic.user import UsersLogic
from ...business_logic.friend import FriendsLogic
from ...business_logic.pull import PullPlayersLogic
from ...business_logic.game import GamesLogic

from copy import deepcopy

from ...repository import UsersCRUD, FriendsCRUD, GamesCRUD, PullPlayersCRUD

from unittest.mock import MagicMock

from .user_builder import UserBuilder

class UsersLogicTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        manager = UsersCRUD()

        # act for test_create_note
        cls.user = UserBuilder('den', '123').with_first_name(MagicMock()).with_last_name(MagicMock()).\
            with_email(MagicMock()).with_phone(MagicMock()).with_about(MagicMock())

        cls.logic = UsersLogic()

        cls.signin = {
            'username': cls.user.user.user.username,
            'password': cls.user.user.user.password
        }

    def test_users_signup_check(self):
        self.assertFalse(self.logic.users_signup_check(self.user.user.user.username))
        self.assertTrue(self.logic.users_signup_check('not den'))

    def test_users_signin_check(self):
        self.assertTrue(self.logic.users_signin_check(self.signin))
        self.assertFalse(self.logic.users_signin_check({'username': self.signin['username'], 'password': '321'}))

    def test_pk_is_users(self):
        self.assertTrue(self.logic.pk_is_users(self.user.user.user, self.user.user.pk))
        self.assertFalse(self.logic.pk_is_users(self.user.user.user, self.user.user.pk + 1))


class FriendsLogicTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # arrange

        data1 = {
            'user': {
                'username': 'den',
                'first_name': 'denis',
                'last_name': 'reling',
                'email': 'reling@reling.com',
                'password': '123'
            },
            'phone': '1111111',
            'about': 'infoooooo',
        }

        data2 = {
            'user': {
                'username': 'den2',
                'first_name': 'denis2',
                'last_name': 'reling2',
                'email': 'reling2@reling.com',
                'password': '123'
            },
            'phone': '11111112',
            'about': 'infoooooo2',
        }

        users_manager = UsersCRUD()
        cls.user1_object = users_manager.create_note(data1)
        cls.user2_object = users_manager.create_note(data2)

        cls.manager = FriendsCRUD()
        cls.logic = FriendsLogic()

        cls.friendship = cls.manager.create_note(cls.user1_object.pk, cls.user2_object.user.pk)

    def test_friend_exists(self):
        self.assertTrue(self.logic.friend_exists(self.friendship.friend.pk, self.friendship.user_friend.user.pk))
        self.assertFalse(self.logic.friend_exists(self.friendship.user_friend.pk, self.friendship.friend.user.pk))

    def test_is_reverse(self):
        self.assertTrue(self.logic.is_reverse(reverse=True))
        self.assertFalse(self.logic.is_reverse(reverse=False))

    def test_not_ready(self):
        # assert
        self.assertFalse(self.logic.friend_ready(self.friendship.user_friend.pk, self.friendship.friend.pk))

    def test_friend_ready(self):
        #act
        self.manager.update_note(self.friendship.friend.pk, self.friendship.user_friend.user.pk, ready_to_play=True)

        #assert
        self.assertTrue(self.logic.friend_ready(self.friendship.user_friend.pk, self.friendship.friend.pk))


class GamesLogicTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # arrange
        data1 = {
            'user': {
                'username': 'den',
                'first_name': 'denis',
                'last_name': 'reling',
                'email': 'reling@reling.com',
                'password': '123'
            },
            'phone': '1111111',
            'about': 'infoooooo',
        }

        data2 = {
            'user': {
                'username': 'den2',
                'first_name': 'denis2',
                'last_name': 'reling2',
                'email': 'reling2@reling.com',
                'password': '123'
            },
            'phone': '11111112',
            'about': 'infoooooo2',
        }

        users_manager = UsersCRUD()
        cls.user1_object = users_manager.create_note(data1)
        cls.user2_object = users_manager.create_note(data2)

        cls.manager = GamesCRUD()

        cls.game_data = {
            'player_1_id': cls.user1_object.pk,
            'player_2_id': cls.user2_object.pk,
            'game_state': {
                'turn': '1',
                'columns': 3,
                'rows': 3,
                'table_with_chips': '000000000'
            }
        }

        # act for test_create_note
        cls.object = cls.manager.create_note(cls.game_data)

        cls.logic = GamesLogic()

    def test_start_game(self):
        #act
        data = self.logic.start_game(self.game_data)

        #assert
        self.assertEqual(data['game_state']['status'], '-1')
        self.assertEqual(data['game_state']['player_1_points'], 0)
        self.assertEqual(data['game_state']['player_2_points'], 0)


    def test_game_exists(self):
        self.assertTrue(self.logic.game_exists(self.object.pk))
        self.assertFalse(self.logic.game_exists(self.object.pk + 1))

    def test_game_is_users(self):
        self.assertTrue(self.logic.game_is_users(self.user1_object.user, self.object.pk))
        self.assertTrue(self.logic.game_is_users(self.user2_object.user, self.object.pk))


class PullPlayersLogicTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # arrange
        user = {
            'user': {
                'username': 'den',
                'first_name': 'denis',
                'last_name': 'reling',
                'email': 'reling@reling.com',
                'password': '123'
            },
            'phone': '1111111',
            'about': 'infoooooo',
        }

        users_manager = UsersCRUD()
        cls.user_object = users_manager.create_note(user)

        user2 = {
            'user': {
                'username': 'den2',
                'first_name': 'denis2',
                'last_name': 'reling2',
                'email': 'reling2@reling.com',
                'password': '123'
            },
            'phone': '11111112',
            'about': 'infoooooo2',
        }

        cls.user2_object = users_manager.create_note(user2)

        cls.manager = PullPlayersCRUD()

        # act for test_create_note
        cls.pull_player = cls.manager.create_note(cls.user_object.user.pk)

        cls.logic = PullPlayersLogic()

    def test_user_in_pull(self):
        self.assertTrue(self.logic.user_in_pull(self.user_object.user.pk))
        self.assertFalse(self.logic.user_in_pull(self.user2_object.user.pk))
