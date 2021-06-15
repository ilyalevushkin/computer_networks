part of 'game_bloc.dart';

enum GameStatus { initial, success, failure }

class GameState extends Equatable {
  const GameState({
    required this.currentBoard,
    required this.lastTurnId,
    required this.firstPlayerMakeTurn,
    this.status = GameStatus.initial,
    this.player1Turns = const <Turn>[],
    this.player2Turns = const <Turn>[]
  });

  final GameStatus status;
  final Board currentBoard;
  final int lastTurnId;
  final int firstPlayerMakeTurn;
  final List<Turn> player1Turns;
  final List<Turn> player2Turns;

  GameState copyWith({
    List<Turn>? player1Turns,
    List<Turn>? player2Turns,
    Board? currentBoard,
    int? lastTurnId,
    GameStatus? status,
    int? firstPlayerMakeTurn
  }) {
    return GameState(
        currentBoard: currentBoard ?? this.currentBoard,
        status: status ?? this.status,
        lastTurnId: lastTurnId ?? this.lastTurnId,
        player1Turns: player1Turns ?? this.player1Turns,
        player2Turns: player2Turns ?? this.player2Turns,
        firstPlayerMakeTurn: firstPlayerMakeTurn ?? this.firstPlayerMakeTurn
    );
  }

  @override
  String toString() {
    return '''GameState {status:${status}
    }''';
  }

  @override
  List<Object> get props => [currentBoard, player1Turns, player2Turns, status,
    firstPlayerMakeTurn];
}