import 'dart:async';
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';

import 'package:flutter_squares/features/game/models/models.dart';

part 'game_event.dart';
part 'game_state.dart';

class GameBloc extends Bloc<GameEvent, GameState> {

  GameBloc(): super(GameState(currentBoard: Board(
    playerTurn: 1,
    rows: 11,
    columns: 11)));

  @override
  Stream<GameState> mapEventToState(
      GameEvent event,
      ) async* {
    if (event is BoardRequested) {
      yield _mapBoardRequestedToState(event, state);
    } else if (event is PlayerListRequested) {
      yield _mapPlayerListRequestedToState(event, state);
    } else if (event is TurnMade) {
      yield _mapTurnMadeToState(event, state);
    } else if (event is SwitchBoard) {
      yield _mapSwitchBoardToState(event, state);
    } else if (event is EnableBoard) {
      yield _mapEnableBoardToState(event, state);
    } else if (event is DisableBoard) {
      yield _mapDisableBoardToState(event, state);
    }
  }

  GameState _mapBoardRequestedToState(GameEvent event, GameState state) {
    return state.copyWith(

    );
  }

  GameState _mapPlayerListRequestedToState(GameEvent event, GameState state) {
    return state.copyWith(

    );
  }

  GameState _mapTurnMadeToState(GameEvent event, GameState state) {
    return state.copyWith(

    );
  }

  GameState _mapSwitchBoardToState(GameEvent event, GameState state) {
    return state.copyWith(

    );
  }

  GameState _mapEnableBoardToState(GameEvent event, GameState state) {
    return state.copyWith(

    );
  }

  GameState _mapDisableBoardToState(GameEvent event, GameState state) {
    return state.copyWith(

    );
  }
}

