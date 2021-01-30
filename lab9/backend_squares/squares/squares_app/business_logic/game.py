from ..models import Games
from .user import UsersLogic
from .friend import FriendsLogic
from .pull import PullPlayersLogic

from ..repository import FriendsCRUD, PullPlayersCRUD, UsersCRUD

from datetime import datetime
from copy import deepcopy

class GamesLogic:
    def __init__(self):
        self.objects = Games.objects
        self.users_logic = UsersLogic()
        self.users_manager = UsersCRUD()
        self.friends_logic = FriendsLogic()
        self.pull_players_logic = PullPlayersLogic()
        self.friends_manager = FriendsCRUD()
        self.pull_players_manager = PullPlayersCRUD()

    def start_game(self, data):
        state = data['game_state']
        state.update({'status': '-1'})
        state.update({'player_1_points': 0})
        state.update({'player_2_points': 0})
        data.update({'game_state': state})
        return data

    def user_is_admin(self, user):
        return self.users_logic.user_is_admin(user)

    def is_active(self, active):
        return active

    def is_user_valid(self, player_id, user_id, user_player_id):
        users = self.users_manager.get_note_by_user_pk(user_id)
        # корректно ли введен id
        if player_id != -1:
            # совпадает ли 2 игрок с тем, кто начинает игру
            if users.id == user_player_id:
                # есть ли я у друга в друзьях (подписан ли он на меня)
                # готов ли он играть
                if self.friends_logic.friend_exists2(users.id, player_id) and \
                        self.friends_logic.friend_ready(player_id, users.id):
                    # отменяем готовность друга
                    self.friends_manager.update_note2(users.id, player_id, False)
                    return True
                elif self.pull_players_logic.user_in_pull2(player_id):
                    # убираем из пула друга, чтобы начать игру
                    self.pull_players_manager.delete_note2(player_id)
                    return True
        return False

    def game_exists(self, game_id):
        return self.objects.is_game_exists(game_id)

    def game_is_users(self, user, game_id):
        users = self.users_manager.get_note_by_user_pk(user.id)
        return self.objects.is_game_users(users.id, game_id)


    def game_state_check(self, prev_state, data, user_player):
        # проверяем, соответствует ли новая фишка фишке игрока
        if data['value'] == user_player:
            # проверяем не выходят ли за границы row_pos и column_pos
            if data['row_pos'] < prev_state.rows and data['column_pos'] < prev_state.columns:
                # проверяем, занята ли выбранная фишка
                if prev_state.table_with_chips[data['row_pos'] * prev_state.columns + data['column_pos']] == '0':
                    return True

        return False

    def update_game_is_correct(self, user, game_id, data):
        users = self.users_manager.get_note_by_user_pk(user.id)
        previous_game_state = self.objects.get_note(game_id)
        # узнаем, кто делает запрос - player_1 или player_2
        user_player = '1'
        if previous_game_state.player_2.id == users.id:
            user_player = '2'
        # проверка на turn юзера (его ход или нет)
        if previous_game_state.game_state.turn == user_player:
            # проверка изменения состояния игры (game_state)
            if self.game_state_check(previous_game_state.game_state, data, user_player):
                return True
        return False


    def calculate_score(self, table, value):
        return table.count(value)

    def make_turn(self, game_id, data):
        prev_game = self.objects.get_note(game_id)
        pos = data['row_pos'] * prev_game.game_state.columns + data['column_pos']
        # ставим фишку
        table = prev_game.game_state.table_with_chips
        table = table[:pos] + data['value'] + table[pos + 1:]
        prev_game.game_state.table_with_chips = table
        # пересчитываем очки
        new_score = self.calculate_score(prev_game.game_state.table_with_chips, data['value'])
        # узнаем, кому пересчитывать очки
        if data['value'] == '1':
            prev_game.game_state.player_1_points = new_score
            # меняем turn на противоположный
            prev_game.game_state.turn = '2'
        else:
            prev_game.game_state.player_2_points = new_score
            prev_game.game_state.turn = '1'
        # проверяем, закончилась ли игра
        if prev_game.game_state.table_with_chips.find('0') == -1:
            prev_game.date_time_to = datetime.now()
            # объявляем победителя
            if prev_game.game_state.player_1_points > prev_game.game_state.player_2_points:
                prev_game.game_state.status = '1'
            elif prev_game.game_state.player_1_points < prev_game.game_state.player_2_points:
                prev_game.game_state.status = '2'
            else:
                prev_game.game_state.status = '0'
        return prev_game

