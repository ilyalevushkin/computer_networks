from http import HTTPStatus
from django.test import TestCase
import os
from copy import deepcopy
import json

from django.contrib.auth.models import User

from ...models import Users, PullPlayers, Games

class GameWithPoolUserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #arrange
        cls.passed = 0

        cls.user1_data = {'User': {
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

        cls.login_data1 = {'User_signin': {
            'username': cls.user1_data['User']['user']['username'],
            'password': cls.user1_data['User']['user']['password']
        }}

        cls.user2_data = {'User': {
            'user': {
                'username': 'den2',
                'first_name': 'denis2',
                'last_name': 'reling2',
                'email': 'reling2@reling.com',
                'password': '123'
            },
            'phone': '11111112',
            'about': 'infoooooo2'
        }}

        cls.login_data2 = {'User_signin': {
            'username': cls.user2_data['User']['user']['username'],
            'password': cls.user2_data['User']['user']['password']
        }}

        cls.game_data = {'Game': {
            'player_1_id': None,
            'player_2_id': None,
            'game_state': {
                'turn': '1',
                'columns': 1,
                'rows': 2,
                'table_with_chips': '00'
            }
        }}

        cls.patch_data = {
            'Game_state_update': {
                'column_pos': 0,
                'row_pos': None,
                'value': ''
            }
        }

    def passedPercent(self):
        print(f'{self.passed}/{self.n}')

    def create_user(self, person):
        data = self.user1_data
        if person == 2:
            data = self.user2_data

        response = self.client.post('/api/v1/users/signup', data=json.dumps(data),
                                    content_type='application/json')

        return response

    def login_user(self, person):
        data = self.login_data1
        if person == 2:
            data = self.login_data2

        response = self.client.post('/api/v1/users/signin', data=json.dumps(data),
                                    content_type='application/json')
        return response

    def get_user_info(self, person, token):
        data = self.get_user_by_username(self.user1_data['User']['user']['username'])
        if person == 2:
            data = self.get_user_by_username(self.user2_data['User']['user']['username'])

        response = self.client.get('/api/v1/users/' + str(data.pk), HTTP_AUTHORIZATION=('Token ' + token))
        return response

    def search_users_in_pull(self, token):
        return self.client.get('/api/v1/pull_players', HTTP_AUTHORIZATION=('Token ' + token))

    def add_user_in_pull(self, token):
        return self.client.post('/api/v1/pull_players', HTTP_AUTHORIZATION=('Token ' + token))

    def start_game(self, person_by, first_turn, token):
        data = self.game_data
        data['Game']['game_state']['turn'] = str(first_turn)
        data['Game']['player_2_id'] = self.get_user_by_username(self.user1_data['User']['user']['username']).pk
        data['Game']['player_1_id'] = self.get_user_by_username(self.user2_data['User']['user']['username']).pk
        if person_by == 2:
            data['Game']['player_2_id'], data['Game']['player_1_id'] = data['Game']['player_1_id'], \
                                                                       data['Game']['player_2_id']
        return self.client.post('/api/v1/games', data=json.dumps(data),
                                    content_type='application/json', HTTP_AUTHORIZATION=('Token ' + token))

    def get_game_by_user(self, person_by, token):
        user = self.get_user_by_username(self.user1_data['User']['user']['username'])
        if person_by == 2:
            user = self.get_user_by_username(self.user2_data['User']['user']['username'])
        return self.client.get('/api/v1/games/users/' + str(user.pk) + '?active=1', HTTP_AUTHORIZATION=('Token ' + token))

    def make_turn(self, game_id, position, person, token):
        data = self.patch_data
        data['Game_state_update']['row_pos'] = position
        data['Game_state_update']['value'] = str(person)
        return self.client.patch('/api/v1/games/' + str(game_id), data=json.dumps(data),
                                    content_type='application/json', HTTP_AUTHORIZATION=('Token ' + token))

    def logout_user(self, token):
        return self.client.get('/api/v1/users/signout', HTTP_AUTHORIZATION=('Token ' + token))

    def get_user_by_username(self, username):
        return Users.objects.get(user__username=username)


    def test_live(self):
        self.n = int(os.getenv('TEST_REPEATS', 100))
        self.passed = 0

        for i in range(self.n):
            self.__test_live()

        self.passedPercent()

    def __test_live(self):
        # create 2 users
        # act
        response = self.create_user(person=1)

        #assert
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(self.get_user_by_username(self.user1_data['User']['user']['username']).user.username,
                    self.user1_data['User']['user']['username'])

        #act
        response = self.create_user(person=2)

        # assert
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(self.get_user_by_username(self.user2_data['User']['user']['username']).user.username,
                self.user2_data['User']['user']['username'])

        # login user1 and user2
        #act
        response = self.login_user(person=1)
        user1_token = response.data['Token']

        #assert
        self.assertEqual(response.status_code, HTTPStatus.OK)

        #act
        response = self.login_user(person=2)
        user2_token = response.data['Token']

        #assert
        self.assertEqual(response.status_code, HTTPStatus.OK)


        # search info about user1 and user2
        #act
        response = self.get_user_info(person=1, token=user1_token)

        #assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['User']['user']['username'], self.user1_data['User']['user']['username'])

        # act
        response = self.get_user_info(person=2, token=user2_token)

        # assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['User']['user']['username'], self.user2_data['User']['user']['username'])

        # search users in pull by user1
        #act
        response = self.search_users_in_pull(token=user1_token)

        #assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data['Pull_players']), 0)

        # add user1 to pull
        # act
        response = self.add_user_in_pull(token=user1_token)

        # assert
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        # search users in pull by user2
        # act
        response = self.search_users_in_pull(token=user2_token)

        # assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data['Pull_players']), 1)
        self.assertEqual(response.data['Pull_players'][0]['player']['user']['username'],
                         self.user1_data['User']['user']['username'])

        # start game with user1 by user2
        # act
        response = self.start_game(person_by=2, first_turn=2, token=user2_token)
        user2_game_id = response.data['Game']['id']

        # assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['Game']['game_state']['table_with_chips'],
                         self.game_data['Game']['game_state']['table_with_chips'])

        # get game_info by user1
        # act
        response = self.get_game_by_user(person_by=1, token=user1_token)
        user1_game_id = response.data['Game']['id']

        # assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['Game']['player_1']['user']['username'],
                         self.user1_data['User']['user']['username'])
        self.assertEqual(response.data['Game']['player_2']['user']['username'],
                         self.user2_data['User']['user']['username'])
        self.assertEqual(response.data['Game']['game_state']['turn'], '2')
        self.assertEqual(user1_game_id, user2_game_id)

        # user2 make turn
        # act
        response = self.make_turn(game_id=user2_game_id, position=0, person=2, token=user2_token)

        # assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['Game']['game_state']['table_with_chips'], '20')
        self.assertEqual(response.data['Game']['game_state']['turn'], '1')
        self.assertEqual(response.data['Game']['game_state']['status'], '-1')

        # user1 make turn and tied
        # act
        response = self.make_turn(game_id=user2_game_id, position=1, person=1, token=user1_token)

        # assert
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['Game']['game_state']['table_with_chips'], '21')
        self.assertEqual(response.data['Game']['game_state']['turn'], '2')
        self.assertEqual(response.data['Game']['game_state']['status'], '0')

        # logout user1 and user2
        # act
        response = self.logout_user(token=user1_token)

        # assert
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # act
        response = self.logout_user(token=user2_token)

        # assert
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # проверка, вышли ли users
        # act
        response = self.logout_user(token=user1_token)

        # assert
        self.assertNotEqual(response.status_code, HTTPStatus.OK)

        # act
        response = self.logout_user(token=user2_token)

        # assert
        self.assertNotEqual(response.status_code, HTTPStatus.OK)

        # Total
        self.passed += 1

        # Cleanup
        Games.objects.all().delete()
        PullPlayers.objects.all().delete()
        Users.objects.all().delete()
        User.objects.all().delete()
