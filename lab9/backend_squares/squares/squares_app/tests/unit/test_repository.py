from django.test import TestCase

from ...repository import UsersCRUD, FriendsCRUD, GamesCRUD, PullPlayersCRUD

from ...serializers.user import UsersSerializer, UsersUpdateSerializer

from ...serializers.game import GamesSerializer

from copy import deepcopy

class UsersCRUDTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #arrange
        cls.data = {
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

        cls.update_data = {
            'phone': '22222222'
        }

        cls.manager = UsersCRUD()

        # act for test_create_note
        cls.object = cls.manager.create_note(deepcopy(cls.data))

    def test_create_note(self):
        #act (в setUpTestData)

        #assert
        self.assertEqual(self.data['user']['username'], self.object.user.username)
        self.assertEqual(self.data['user']['password'], self.object.user.password)
        self.assertEqual(self.data['phone'], self.object.phone)

    def test_get_note(self):
        #act
        get_object = self.manager.get_note(self.object.pk)

        #assert
        self.assertEqual(self.object, get_object)

    def test_update_note(self):
        #act
        update_object = self.manager.update_note(self.update_data, self.object.pk)

        #assert
        self.assertNotEqual(self.object.phone, update_object.phone)


class FriendsCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #arrange

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

        #act for test_create_note
        cls.friendship = cls.manager.create_note(cls.user1_object.pk, cls.user2_object.user.pk)

    def test_create_note(self):
        #act

        #assert
        self.assertEqual(self.friendship.user_friend.pk, self.user2_object.pk)
        self.assertEqual(self.friendship.friend.pk, self.user1_object.pk)
        self.assertEqual(self.friendship.status, 'Нет')

    def test_get_note(self):
        #act
        get_object = self.manager.get_note(self.friendship.friend.pk, self.friendship.user_friend.user.pk,
                                           reverse=False)

        #assert
        self.assertEqual(self.friendship, get_object)

    def test_update_note(self):
        #act
        update_object = self.manager.update_note(self.friendship.friend.pk, self.friendship.user_friend.user.pk,
                                                 ready_to_play=True)

        #assert
        self.assertEqual(update_object.status, 'Да')


class GamesCRUDTest(TestCase):
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

        cls.update_data = deepcopy(cls.game_data)
        cls.update_data['game_state']['turn'] = '2'
        cls.update_data['game_state']['table_with_chips'] = '000000001'

    def test_create_note(self):
        #act (в setUpTestData)

        #assert
        self.assertEqual(self.game_data['player_1_id'], self.object.player_1_id)
        self.assertEqual(self.game_data['player_2_id'], self.object.player_2_id)
        self.assertEqual(self.game_data['game_state']['table_with_chips'], self.object.game_state.table_with_chips)

    def test_get_note(self):
        #act
        get_object = self.manager.get_note(self.object.pk)

        #assert
        self.assertEqual(self.object, get_object)

    def test_update_note(self):
        #act
        update_object = self.manager.update_note(deepcopy(self.update_data), self.object.pk)

        #assert
        self.assertEqual(self.update_data['game_state']['turn'], update_object.game_state.turn)
        self.assertEqual(self.update_data['game_state']['table_with_chips'], update_object.game_state.table_with_chips)


class PullPlayersCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #arrange

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

        cls.manager = PullPlayersCRUD()

        #act for test_create_note
        cls.pull_player = cls.manager.create_note(cls.user_object.user.pk)

    def test_create_note(self):
        #act

        #assert
        self.assertEqual(self.pull_player.player.pk, self.user_object.pk)

    def test_get_note(self):
        #act
        get_object = self.manager.get_note(self.pull_player.player.user.pk)

        #assert
        self.assertEqual(self.pull_player, get_object)

    def test_delete_note(self):
        #act
        self.manager.delete_note(self.pull_player.player.user.pk)

        #assert
        throw_exception = False

        try:
            self.manager.get_note(self.pull_player.player.user.pk)
        except:
            throw_exception = True

        self.assertTrue(throw_exception)
