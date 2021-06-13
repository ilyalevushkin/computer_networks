part of 'game_bloc.dart';

enum GameStatus { initial, success, failure }

class GameState extends Equatable {
  const GameState({
    required this.currentBoard,
    this.status = GameStatus.initial,
    this.player1Turns = const <Turn>[],
    this.player2Turns = const <Turn>[],
    this.currentTurn = const Turn(id: -1)
  });

  final GameStatus status;
  final Board currentBoard;
  final Turn currentTurn;
  final List<Turn> player1Turns;
  final List<Turn> player2Turns;

  GameState copyWith({
  List<Turn>? player1Turns,
  List<Turn>? player2Turns,
    Board? currentBoard,
    GameStatus? status,
    Turn? currentTurn
  }) {
    return GameState(
      currentBoard: currentBoard ?? this.currentBoard,
      status: status ?? this.status,
      player1Turns: player1Turns ?? this.player1Turns,
      player2Turns: player2Turns ?? this.player2Turns,
      currentTurn: currentTurn ?? this.currentTurn
    );
  }

  @override
  String toString() {
    return '''GameState {status:${status}
    }''';
  }

  @override
  List<Object> get props => [currentBoard, player1Turns, player2Turns, status,
  currentTurn];
}