import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';
import 'package:flutter_squares/features/game/models/turn.dart';

class Board extends Equatable {

  Board({required this.playerTurn,
    required this.rows,
    required this.columns,
    required this.lastTurn,
    this.enabled = true,
    this.totalScorePlayer1 = 0,
    this.totalScorePlayer2 = 0,
    this.board = const [],
    this.isFull = false
  }) {
    if (this.board.isEmpty) {
      this.board = List.generate(this.rows,
              (index) => List.generate(this.columns, (index) => 0, growable: false),
          growable: false);
    }
  }

  final int playerTurn;
  final Turn lastTurn;
  final int rows;
  final int columns;
  int totalScorePlayer1;
  int totalScorePlayer2;
  final bool enabled;
  final bool isFull;
  List<List<int>> board;

  @override
  List<Object> get props => [rows, columns, totalScorePlayer1,
    totalScorePlayer2, playerTurn, board, lastTurn, isFull];
}