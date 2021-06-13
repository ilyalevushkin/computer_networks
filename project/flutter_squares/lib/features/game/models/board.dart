import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';

class Board extends Equatable {

  Board({required this.playerTurn,
    required this.rows,
    required this.columns,
    this.enabled = true,
    this.board = const []
  }) {
    this.board = List.generate(this.rows,
        (index) => List.generate(this.columns, (index) => 0, growable: false),
        growable: false);
  }

  final int playerTurn;
  final int rows;
  final int columns;
  final bool enabled;
  List<List<int>> board;

  @override
  List<Object> get props => [rows, columns, playerTurn, board];
}