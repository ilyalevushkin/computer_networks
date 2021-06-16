import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class GameResults extends StatelessWidget {

  final int scorePlayer1;
  final int scorePlayer2;

  GameResults({required this.scorePlayer1,
    required this.scorePlayer2});

  @override
  Widget build(BuildContext context) {
    final theme = context.read<ITheme>();
    String winner;
    if (scorePlayer1 > scorePlayer2) {
      winner = 'Winner: Player 1';
    }
    else if (scorePlayer2 > scorePlayer1) {
      winner = 'Winner: Player 2';
    }
    else {
      winner = 'Draw';
    }
    return Container(
      alignment: Alignment.center,
      height: 300,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(18.0),
        color: Colors.white
      ),
      child: Text(winner,
      style: theme.gameResultsTheme.playerNameTextStyle,),
    );
  }
}