part of 'game_bloc.dart';

abstract class GameEvent extends Equatable {
  const GameEvent();

  @override
  List<Object> get props => [];
}

class BoardRequested extends GameEvent {}

class PlayerListRequested extends GameEvent {
  const PlayerListRequested(this.player);

  final int player;

  @override
  List<Object> get props => [player];
}

class TurnMade extends GameEvent {
  const TurnMade(this.turn);

  final Turn turn;

  @override
  List<Object> get props => [turn];
}

class SwitchBoard extends GameEvent {
  const SwitchBoard(this.turnId);

  final int turnId;

  @override
  List<Object> get props => [turnId];
}

class EnableBoard extends GameEvent {}

class DisableBoard extends GameEvent {}