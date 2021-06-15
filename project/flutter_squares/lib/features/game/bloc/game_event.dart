part of 'game_bloc.dart';

abstract class GameEvent extends Equatable {
  const GameEvent();

  @override
  List<Object> get props => [];
}

class BoardRequested extends GameEvent {}

class InitialTurnMade extends GameEvent {}

class TurnMade extends GameEvent {
  const TurnMade(this.rowPos, this.columnPos);

  final int rowPos;
  final int columnPos;

  @override
  List<Object> get props => [rowPos, columnPos];
}

class SwitchBoard extends GameEvent {
  const SwitchBoard(this.turnId);

  final int turnId;

  @override
  List<Object> get props => [turnId];
}