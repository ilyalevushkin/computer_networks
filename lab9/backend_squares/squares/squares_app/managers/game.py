from django.db import models

from ..models import GameStates

from datetime import datetime

class GamesManager(models.Manager):

    def get_all(self):
        return self.all()

    def get_note(self, pk):
        return self.get(pk=pk)

    def get_notes(self, status):
        return self.filter(game_state__status=status)

    def get_notes_by_users_pk(self, users_pk, status):
        query1 = self.filter(player_1__pk=users_pk)
        query2 = self.filter(player_2__pk=users_pk)
        mix_query = query1 | query2
        if status == '-1':
            mix_query = mix_query.filter(game_state__status=status)
        return mix_query

    def create_note(self, data, user, friend):
        game_state = GameStates.objects.create(**data['game_state'])
        #data.pop('player_1_id')
        #data.pop('player_2_id')
        #data.update({'player_1': friend})
        #data.update({'player_2': user})
        #data.pop('game_state')
        #data.update({'game_state_id': game_state})
        #print(data)
        game = self.create(player_1=friend, player_2=user, game_state=game_state)
        #game.save()
        return game

    def update_note_by_dict(self, note, d):
        for key, value in d.items():
            setattr(note, key, value)
        note.save()

    def update_note(self, data, pk):
        game = self.get(pk=pk)
        game_state = GameStates.objects.get(pk=game.game_state.pk)
        self.update_note_by_dict(game_state, data['game_state'])
        data.pop('game_state')
        return self.get(pk=pk)

    def delete_note(self, pk):
        game = self.get_note(pk)
        game.delete()

    def is_game_exists(self, pk):
        return self.filter(pk=pk).exists()

    def is_game_users(self, player_pk, pk):
        game = self.get_note(pk)
        return game.player_1.pk == player_pk or game.player_2.pk == player_pk
