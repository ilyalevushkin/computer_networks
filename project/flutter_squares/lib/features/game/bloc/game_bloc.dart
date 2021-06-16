import 'dart:async';
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';

import 'package:flutter_squares/features/game/models/models.dart';
import 'package:flutter_squares/features/game/view/player_list.dart';

part 'game_event.dart';
part 'game_state.dart';

class GameBloc extends Bloc<GameEvent, GameState> {

  GameBloc({
    this.rows = 8,
    this.columns = 8,
    this.playerTurn = 1
  }): super(GameState(currentBoard: Board(
    playerTurn: playerTurn,
    rows: rows,
    columns: columns,
    lastTurn: Turn(
      id: -1,
      player: playerTurn == 1 ? 2 : 1,
      rowPos: -1,
      columnPos: -1,
      addScore: 0
    ),
    enabled: true),
    lastTurnId: -1,
    firstPlayerMakeTurn: playerTurn)) {
    this.add(InitialTurnMade());
    this.add(BoardRequested());
  }

  final int rows;
  final int columns;
  final int playerTurn;

  @override
  Stream<GameState> mapEventToState(
      GameEvent event,
      ) async* {
    if (event is BoardRequested) {
      yield _mapBoardRequestedToState(event, state);
    } else if (event is TurnMade) {
      yield _mapTurnMadeToState(event, state);
    } else if (event is InitialTurnMade) {
      yield _mapInitialTurnMadeToState(event, state);
    } else if (event is SwitchBoard) {
      yield _mapSwitchBoardToState(event, state);
    }
  }

  GameState _mapInitialTurnMadeToState(InitialTurnMade event, GameState state) {
    return this.state.copyWith(
      player1Turns: [this.state.currentBoard.lastTurn],
      player2Turns: [this.state.currentBoard.lastTurn],
    );
  }

  GameState _mapBoardRequestedToState(BoardRequested event, GameState state) {
    return state.copyWith(
      status: GameStatus.success
    );
  }

  bool isBoardFulled(List<List<int>> board) {
    for (int i = 0; i < board.length; i++) {
      if (board[i].contains(0)) {
        return false;
      }
    }
    return true;
  }

  Board updateBoard(Turn newTurn, Board currentBoard) {
    currentBoard.board[newTurn.rowPos][newTurn.columnPos] = newTurn.player;
    return Board(playerTurn: newTurn.player == 1 ? 2 : 1,
        rows: currentBoard.rows,
        columns: currentBoard.columns,
        lastTurn: newTurn,
        board: currentBoard.board,
        isFull: isBoardFulled(currentBoard.board),
        totalScorePlayer1: currentBoard.totalScorePlayer1,
        totalScorePlayer2: currentBoard.totalScorePlayer2);
  }

  bool isPosInBoardShape(pos, int rows) {
    return ((pos < rows) && (pos >= 0));
  }

  Map<String, List<int>> getSquareCorners(int leftDownRowPos, int leftDownColumnPos,
      int rightUpRowPos, int rightUpColumnPos, bool diagonal) {
    Map<String, List<int>> square = {
      'Rows': [],
      'Columns': []
    };
    if (diagonal) {
      int middleDownRowPos = leftDownRowPos;
      int middleDownColumnPos = leftDownColumnPos + (rightUpColumnPos - leftDownColumnPos) ~/ 2;

      int middleUpRowPos = rightUpRowPos;
      int middleUpColumnPos = middleDownColumnPos;

      int leftMiddleRowPos = leftDownRowPos + (rightUpRowPos - leftDownRowPos) ~/ 2;
      int leftMiddleColumnPos = leftDownColumnPos;

      int rightMiddleRowPos = leftMiddleRowPos;
      int rightMiddleColumnPos = rightUpColumnPos;
      square['Rows']!.addAll([middleDownRowPos, middleUpRowPos,
        leftMiddleRowPos, rightMiddleRowPos]);
      square['Columns']!.addAll([middleDownColumnPos, middleUpColumnPos,
        leftMiddleColumnPos, rightMiddleColumnPos]);
    }
    else {
      int leftUpRowPos = rightUpRowPos;
      int leftUpColumnPos = leftDownColumnPos;

      int rightDownRowPos = leftDownRowPos;
      int rightDownColumnPos = rightUpColumnPos;
      square['Rows']!.addAll([leftDownRowPos, rightUpRowPos,
        leftUpRowPos, rightDownRowPos]);
      square['Columns']!.addAll([leftDownColumnPos, rightUpColumnPos,
        leftUpColumnPos, rightDownColumnPos]);
    }
    return square;
  }

  bool isSquare(List<List<int>> board, int playerTurn,
  Map<String, List<int>> square) {
    return (board[square['Rows']![0]][square['Columns']![0]] == playerTurn) &&
        (board[square['Rows']![1]][square['Columns']![1]] == playerTurn) &&
        (board[square['Rows']![2]][square['Columns']![2]] == playerTurn) &&
        (board[square['Rows']![3]][square['Columns']![3]] == playerTurn);
  }

  Turn calcUsualSquares(int rows, int columns, int rowPos, int columnPos,
      int playerTurn, List<List<int>> board, int rowAdd, int columnAdd,
      Turn newTurn) {
    int curRowPos = rowPos + rowAdd;
    int curColumnPos = columnPos + columnAdd;
    while (isPosInBoardShape(curRowPos, rows) &&
        isPosInBoardShape(curColumnPos, columns)) {
      Map<String, List<int>> corners = getSquareCorners(rowPos, columnPos,
          curRowPos, curColumnPos, false);
      if (isSquare(board, playerTurn, corners)) {
        newTurn.addScore += 1 + ((rowPos - curRowPos).abs() - 1) * 2;
        newTurn.addedScoreDotsPos['Rows']!.addAll(corners['Rows']!);
        newTurn.addedScoreDotsPos['Columns']!.addAll(corners['Columns']!);
      }
      curRowPos += rowAdd;
      curColumnPos += columnAdd;
    }
    return newTurn;
  }

  Turn calcScoreAddByTurn(int rowPos, int columnPos, int playerTurn,
  List<List<int>> board, Turn newTurn) {
    int rows = board.length;
    int columns = board[0].length;

    // считаем обычные квадраты
    // идем вправо вверх
    newTurn = calcUsualSquares(rows, columns, rowPos, columnPos,
        playerTurn, board, -1, 1, newTurn);
    // идем вправо вниз
    newTurn = calcUsualSquares(rows, columns, rowPos, columnPos,
        playerTurn, board, 1, 1, newTurn);
    // идем влево вниз
    newTurn = calcUsualSquares(rows, columns, rowPos, columnPos,
        playerTurn, board, 1, -1, newTurn);
    // идем влево вверх
    newTurn = calcUsualSquares(rows, columns, rowPos, columnPos,
        playerTurn, board, -1, -1, newTurn);

    // считаем диагональные квадраты
    // идем вверх
    int curRowPos = rowPos - 1;
    int curColumnPos = columnPos + 1;

    int leftDownRowPos = rowPos;
    int leftDownColumnPos = columnPos - (curColumnPos - columnPos);
    int rightUpRowPos = curRowPos - (rowPos - curRowPos);
    int rightUpColumnPos = curColumnPos;

    while (isPosInBoardShape(leftDownRowPos, rows) &&
        isPosInBoardShape(leftDownColumnPos, columns) &&
        isPosInBoardShape(rightUpRowPos, rows) &&
        isPosInBoardShape(rightUpColumnPos, columns)) {
      Map<String, List<int>> corners = getSquareCorners(leftDownRowPos, leftDownColumnPos,
          rightUpRowPos, rightUpColumnPos, true);
      if (isSquare(board, playerTurn, corners)) {
        newTurn.addScore += 2 + ((rowPos - curRowPos).abs() - 1) * 2;
        newTurn.addedScoreDotsPos['Rows']!.addAll(corners['Rows']!);
        newTurn.addedScoreDotsPos['Columns']!.addAll(corners['Columns']!);
      }
      curRowPos -= 1;
      curColumnPos += 1;

      leftDownRowPos = rowPos;
      leftDownColumnPos = columnPos - (curColumnPos - columnPos);
      rightUpRowPos = curRowPos - (rowPos - curRowPos);
      rightUpColumnPos = curColumnPos;
    }
    // идем вправо
    curRowPos = rowPos + 1;
    curColumnPos = columnPos + 1;

    leftDownRowPos = curRowPos;
    leftDownColumnPos = columnPos;
    rightUpRowPos = rowPos - (curRowPos - rowPos);
    rightUpColumnPos = curColumnPos + (curColumnPos - columnPos);

    while (isPosInBoardShape(leftDownRowPos, rows) &&
        isPosInBoardShape(leftDownColumnPos, columns) &&
        isPosInBoardShape(rightUpRowPos, rows) &&
        isPosInBoardShape(rightUpColumnPos, columns)) {
      Map<String, List<int>> corners = getSquareCorners(leftDownRowPos, leftDownColumnPos,
          rightUpRowPos, rightUpColumnPos, true);
      if (isSquare(board, playerTurn, corners)) {
        newTurn.addScore += 2 + ((rowPos - curRowPos).abs() - 1) * 2;
        newTurn.addedScoreDotsPos['Rows']!.addAll(corners['Rows']!);
        newTurn.addedScoreDotsPos['Columns']!.addAll(corners['Columns']!);
      }
      curRowPos += 1;
      curColumnPos += 1;

      leftDownRowPos = curRowPos;
      leftDownColumnPos = columnPos;
      rightUpRowPos = rowPos - (curRowPos - rowPos);
      rightUpColumnPos = curColumnPos + (curColumnPos - columnPos);
    }
    // идем вниз
    curRowPos = rowPos + 1;
    curColumnPos = columnPos - 1;

    leftDownRowPos = curRowPos + (curRowPos - rowPos);
    leftDownColumnPos = curColumnPos;
    rightUpRowPos = rowPos;
    rightUpColumnPos = columnPos + (columnPos - curColumnPos);

    while (isPosInBoardShape(leftDownRowPos, rows) &&
        isPosInBoardShape(leftDownColumnPos, columns) &&
        isPosInBoardShape(rightUpRowPos, rows) &&
        isPosInBoardShape(rightUpColumnPos, columns)) {
      Map<String, List<int>> corners = getSquareCorners(leftDownRowPos, leftDownColumnPos,
          rightUpRowPos, rightUpColumnPos, true);
      if (isSquare(board, playerTurn, corners)) {
        newTurn.addScore += 2 + ((rowPos - curRowPos).abs() - 1) * 2;
        newTurn.addedScoreDotsPos['Rows']!.addAll(corners['Rows']!);
        newTurn.addedScoreDotsPos['Columns']!.addAll(corners['Columns']!);
      }
      curRowPos += 1;
      curColumnPos -= 1;

      leftDownRowPos = curRowPos + (curRowPos - rowPos);
      leftDownColumnPos = curColumnPos;
      rightUpRowPos = rowPos;
      rightUpColumnPos = columnPos + (columnPos - curColumnPos);
    }
    // идем влево
    curRowPos = rowPos - 1;
    curColumnPos = columnPos - 1;

    leftDownRowPos = rowPos + (rowPos - curRowPos);
    leftDownColumnPos = curColumnPos + (curColumnPos - columnPos);
    rightUpRowPos = curRowPos;
    rightUpColumnPos = columnPos;

    while (isPosInBoardShape(leftDownRowPos, rows) &&
        isPosInBoardShape(leftDownColumnPos, columns) &&
        isPosInBoardShape(rightUpRowPos, rows) &&
        isPosInBoardShape(rightUpColumnPos, columns)) {
      Map<String, List<int>> corners = getSquareCorners(leftDownRowPos, leftDownColumnPos,
          rightUpRowPos, rightUpColumnPos, true);
      if (isSquare(board, playerTurn, corners)) {
        newTurn.addScore += 2 + ((rowPos - curRowPos).abs() - 1) * 2;
        newTurn.addedScoreDotsPos['Rows']!.addAll(corners['Rows']!);
        newTurn.addedScoreDotsPos['Columns']!.addAll(corners['Columns']!);
      }
      curRowPos -= 1;
      curColumnPos -= 1;

      leftDownRowPos = rowPos + (rowPos - curRowPos);
      leftDownColumnPos = curColumnPos + (curColumnPos - columnPos);
      rightUpRowPos = curRowPos;
      rightUpColumnPos = columnPos;
    }
    return newTurn;
  }

  GameState _mapTurnMadeToState(TurnMade event, GameState state) {
    if (state.lastTurnId != state.currentBoard.lastTurn.id) {
      return state.copyWith(status: GameStatus.failure);
    }
    if (!state.currentBoard.enabled) {
      return state.copyWith(status: GameStatus.failure);
    }
    Turn newTurn = Turn(
        id: state.lastTurnId + 1,
        player: state.currentBoard.playerTurn,
        rowPos: event.rowPos,
        columnPos: event.columnPos,
        addScore: 0,
        addedScoreDotsPos: {
          'Rows': [],
          'Columns': []
        });
    Board updateBoard = this.updateBoard(newTurn, state.currentBoard);
    newTurn = calcScoreAddByTurn(event.rowPos,
        event.columnPos, state.currentBoard.playerTurn,
        state.currentBoard.board, newTurn);
    List<Turn> playerTurns = newTurn.player == 1 ? state.player1Turns :
        state.player2Turns;
    playerTurns.add(newTurn);
    if (newTurn.player == 1) {
      updateBoard.totalScorePlayer1 += newTurn.addScore;
      return state.copyWith(
        currentBoard: updateBoard,
        player1Turns: playerTurns,
        lastTurnId: newTurn.id,
      );
    }
    else {
      updateBoard.totalScorePlayer2 += newTurn.addScore;
      return state.copyWith(
          currentBoard: updateBoard,
          player2Turns: playerTurns,
          lastTurnId: newTurn.id
      );
    }
  }

  Turn getTurnById(int turnId, List<Turn> player1Turns,
      List<Turn> player2Turns, int firstPlayerMakeTurn) {
    if (turnId == -1) {
      return player1Turns[0];
    }
    if (firstPlayerMakeTurn == 1) {
      if (turnId.isEven) {
        return player1Turns[turnId ~/ 2 + 1];
      }
      else {
        return player2Turns[(turnId - 1) ~/ 2 + 1];
      }
    } else {
      if (turnId.isEven) {
        return player2Turns[turnId ~/ 2 + 1];
      }
      else {
        return player1Turns[(turnId - 1) ~/ 2 + 1];
      }
    }
  }

  Board? calcCurrentBoard(int switchTurnId, List<Turn> player1Turns,
      List<Turn> player2Turns, Board board, int lastTurnId,
      int firstPlayerMakeTurn) {

    Turn newLastTurn = getTurnById(switchTurnId, player1Turns, player2Turns,
        firstPlayerMakeTurn);

    // отматываем доску
    int newTotalScorePlayer1 = board.totalScorePlayer1;
    int newTotalScorePlayer2 = board.totalScorePlayer2;
    List<List<int>> newBoard = board.board;
    if (switchTurnId > board.lastTurn.id) {
      int newBoardLastTurnId = board.lastTurn.id;
      while (newBoardLastTurnId != switchTurnId) {
        newBoardLastTurnId += 1;
        Turn nextTurn = getTurnById(newBoardLastTurnId, player1Turns, player2Turns,
            firstPlayerMakeTurn);
        if (nextTurn.player == 1) {
          newTotalScorePlayer1 += nextTurn.addScore;
        }
        else {
          newTotalScorePlayer2 += nextTurn.addScore;
        }
        newBoard[nextTurn.rowPos][nextTurn.columnPos] = nextTurn.player;
      }
    }
    else {
      int newBoardLastTurnId = board.lastTurn.id;
      while (newBoardLastTurnId != switchTurnId) {
        Turn lastTurn = getTurnById(newBoardLastTurnId, player1Turns, player2Turns,
            firstPlayerMakeTurn);
        // обновляем доску до предыщущего значения
        newBoard[lastTurn.rowPos][lastTurn.columnPos] = 0;
        if (lastTurn.player == 1) {
          newTotalScorePlayer1 -= lastTurn.addScore;
        }
        else {
          newTotalScorePlayer2 -= lastTurn.addScore;
        }
        newBoardLastTurnId -= 1;
      }
    }
    return Board(playerTurn: newLastTurn.player == 1 ? 2 : 1,
        rows: board.rows,
        columns: board.columns,
        lastTurn: newLastTurn,
        enabled: newLastTurn.id == lastTurnId,
        board: newBoard,
        totalScorePlayer1: newTotalScorePlayer1,
        totalScorePlayer2: newTotalScorePlayer2
    );
  }

  GameState _mapSwitchBoardToState(SwitchBoard event, GameState state) {
    Board? switchedBoard = calcCurrentBoard(event.turnId, state.player1Turns,
    state.player2Turns, state.currentBoard, state.lastTurnId, state.firstPlayerMakeTurn);
    if (switchedBoard == null) {
      return state.copyWith(status: GameStatus.failure);
    }
    return state.copyWith(
      currentBoard: switchedBoard,
    );
  }
}

