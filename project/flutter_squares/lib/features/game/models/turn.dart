import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';

class Turn extends Equatable {

  Turn({
    required this.id,
    required this.player,
    required this.rowPos,
    required this.columnPos,
    required this.addScore
  });

  final int id;
  final int player;
  final int rowPos;
  final int columnPos;
  int addScore;

  @override
  List<Object> get props => [id, player, rowPos, columnPos];
}