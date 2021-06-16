import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_squares/features/game/bloc/game_bloc.dart';
import 'package:flutter_squares/features/game/models/turn.dart';
import 'package:flutter_squares/features/game/widgets/turn.dart';

class PlayerList extends StatelessWidget {

  final String playerName;
  final AnimationController controller;

  PlayerList({required this.playerName,
  required this.controller});

  @override
  Widget build(BuildContext context) {
    final theme = context.read<ITheme>();
    return BlocBuilder<GameBloc, GameState>(
        builder: (context, state) {
            switch (state.status) {
              case GameStatus.failure:
                return const Center(child: Text('failed to load game'));
              case GameStatus.success:
                final List<Turn> reversedTurns = playerName == 'Player 1' ?
                List.from(state.player1Turns.reversed) :
                List.from(state.player2Turns.reversed);
                if (reversedTurns.isEmpty) {
                  return const Center(child: Text('no turns'));
                }

                return Container(
                      padding: EdgeInsets.only(bottom: 24),
                      margin: EdgeInsets.only(left: 8),
                      child: ListView.builder(
                        itemBuilder: (BuildContext context, int index) {
                          Turn turn = reversedTurns[index];
                          return TurnCard(turn: turn,
                              lastTurnId: state.lastTurnId,
                              boardLastTurnId: state.currentBoard.lastTurn.id,
                          controller: controller,);
                        },
                        itemCount: reversedTurns.length,
                        scrollDirection: Axis.horizontal
                      )
                    );

              default:
                return const Center(child: CircularProgressIndicator());
            }
        });
  }
}