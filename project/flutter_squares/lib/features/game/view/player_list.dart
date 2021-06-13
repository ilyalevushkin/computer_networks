import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_squares/features/game/bloc/game_bloc.dart';
import 'package:flutter_squares/features/game/models/turn.dart';
import 'package:flutter_squares/features/game/widgets/turn.dart';

class PlayerList extends StatelessWidget {

  final String player;

  PlayerList({required this.player});

  @override
  Widget build(BuildContext context) {
    final theme = context.read<ITheme>();
    return BlocBuilder<GameBloc, GameState>(
        builder: (context, state) {
            switch (state.status) {
              case GameStatus.failure:
                return const Center(child: Text('failed to load game'));
              case GameStatus.success:
                final List<Turn> turns = player == 'Player 1' ?
                state.player1Turns : state.player2Turns;
                if (turns.isEmpty) {
                  return const Center(child: Text('no turns'));
                }
                return Column(children: [
                    Text(player),
                    Expanded(child: Container(
                      width: 50,
                      margin: EdgeInsets.only(left: 12, top: 22),
                      child: ListView.builder(
                        itemBuilder: (BuildContext context, int index) {
                          Turn turn = turns[index];
                          return TurnCard(turn: turn);
                        },
                        itemCount: turns.length,
                        scrollDirection: Axis.vertical
                      )
                    ))
                  ],
                  );

              default:
                return const Center(child: CircularProgressIndicator());
            }
        });
  }
}