from http import HTTPStatus
from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory
from copy import deepcopy


from ..unit.user_builder import UserBuilder

from ...business_logic.game import GamesLogic


from ...models import Users

from ...repository import UsersCRUD, GamesCRUD

import json


class RegistrationTest(TestCase):
    def test_registration_success(self):
        user_data = {'User': {
            'user': {
                'username': 'den',
                'first_name': 'denis',
                'last_name': 'reling',
                'email': 'reling@reling.com',
                'password': '123'
            },
            'phone': '1111111',
            'about': 'infoooooo'
        }}
        response = self.client.post('/api/v1/users/signup', data=json.dumps(user_data), content_type='application/json')

        try:
            created_user = Users.objects.get(user__username=user_data['User']['user']['username'])
            is_user_created = True
        except:
            created_user = {'user': None}
            is_user_created = False

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(is_user_created)
        self.assertEqual(created_user.user.username, user_data['User']['user']['username'])

    def test_registration_already_exists(self):
        user_data = {
            'user': {
                'username': 'den',
                'first_name': 'denis',
                'last_name': 'reling',
                'email': 'reling@reling.com',
                'password': '123'
            },
            'phone': '1111111',
            'about': 'infoooooo'
        }
        manager = UsersCRUD()

        manager.create_note(user_data)

        response = self.client.post('/api/v1/users/signup', data=json.dumps(user_data), content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)


class PullPlayersTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            'user': {
                'username': 'den',
                'first_name': 'denis',
                'last_name': 'reling',
                'email': 'reling@reling.com',
                'password': '123'
            },
            'phone': '1111111',
            'about': 'infoooooo'
        }

        cls.login_data = {'User_signin': {
            'username': cls.user_data['user']['username'],
            'password': cls.user_data['user']['password']
        }}

    def create_user(self):
        manager = UsersCRUD()
        manager.create_note(deepcopy(self.user_data))

    def login_user(self):
        response = self.client.post('/api/v1/users/signin', data=json.dumps(self.login_data),
                                    content_type='application/json')
        return response.data['Token']

    def test_post_self_to_pull(self):
        self.create_user()
        token = self.login_user()
        response = self.client.post('/api/v1/pull_players', HTTP_AUTHORIZATION=('Token ' + token))

        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_already_in_pull(self):
        self.create_user()
        token = self.login_user()

        self.client.post('/api/v1/pull_players', HTTP_AUTHORIZATION=('Token ' + token))
        response = self.client.post('/api/v1/pull_players', HTTP_AUTHORIZATION=('Token ' + token))

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class GameTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1_data = {
            'user': {
                'username': 'den',
                'first_name': 'denis',
                'last_name': 'reling',
                'email': 'reling@reling.com',
                'password': '123'
            },
            'phone': '1111111',
            'about': 'infoooooo'
        }

        cls.login_data1 = {'User_signin':{
            'username': cls.user1_data['user']['username'],
            'password': cls.user1_data['user']['password']
        }}

        cls.user2_data = {
            'user': {
                'username': 'den2',
                'first_name': 'denis2',
                'last_name': 'reling2',
                'email': 'reling2@reling.com',
                'password': '123'
            },
            'phone': '11111112',
            'about': 'infoooooo2'
        }

        cls.login_data2 = {'User_signin': {
            'username': cls.user2_data['user']['username'],
            'password': cls.user2_data['user']['password']
        }}

        users_manager = UsersCRUD()
        cls.user1_object = users_manager.create_note(cls.user1_data)
        cls.user2_object = users_manager.create_note(cls.user2_data)

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

        cls.patch_data = {
            'Game_state_update': {
                'column_pos': 1,
                'row_pos': 1,
                'value': 1
            }
        }

    def login_user(self, person):
        data = self.login_data1
        if person == 2:
            data = self.login_data2

        response = self.client.post('/api/v1/users/signin', data=json.dumps(data),
                                    content_type='application/json')
        return response.data['Token']


    def create_game(self):
        manager = GamesCRUD()
        return manager.create_note(self.game_data).pk

    @patch('squares_app.business_logic.game.GamesLogic.calculate_score', return_value=10)
    def test_game_update_success(self, mock_method):
        game_pk = self.create_game()
        token = self.login_user(person=1)

        #patch game
        response = self.client.patch('/api/v1/games/' + str(game_pk), data=json.dumps(self.patch_data),
                                    content_type='application/json', HTTP_AUTHORIZATION=('Token ' + token))

        self.assertTrue(mock_method.called)
        self.assertEqual(response.data['Game']['game_state']['table_with_chips'], '000010000')
        self.assertNotEqual(response.data['Game']['game_state']['table_with_chips'], '000000000')
        self.assertEqual(response.data['Game']['game_state']['player_1_points'], 10)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @patch('squares_app.business_logic.game.GamesLogic.calculate_score', return_value=10)
    def test_game_update_user_cheats(self, mock_method):
        game_pk = self.create_game()
        token = self.login_user(person=2)

        # patch game
        response = self.client.patch('/api/v1/games/' + str(game_pk), data=json.dumps(self.patch_data),
                                     content_type='application/json', HTTP_AUTHORIZATION=('Token ' + token))

        self.assertFalse(mock_method.called)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, 'User cheats')
