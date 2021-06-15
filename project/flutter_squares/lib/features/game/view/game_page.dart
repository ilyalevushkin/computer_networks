import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_squares/features/game/bloc/game_bloc.dart';
import 'package:flutter_squares/features/game/view/board.dart';
import 'package:flutter_squares/features/game/view/player_list.dart';
import 'package:flutter_squares/features/game/widgets/score_results.dart';

class GamePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final theme = context.read<ITheme>();
    return BlocProvider(
      create: (context) => GameBloc(),
      child: BlocBuilder<GameBloc, GameState>(
      builder: (context, state) {
        return Align(alignment: Alignment.topCenter,
        child: Container(
          decoration: BoxDecoration(
            color: theme.gamePageTheme.backgroundColor
          ),
          child: Column(
            children: [
              Expanded(flex: 1, child:
                ScoreResult(playerName: 'Player 1',
                  totalPlayerScore: state.currentBoard.totalScorePlayer1,
                  addPlayerScore: state.currentBoard.lastTurn.player == 1 ?
                  state.currentBoard.lastTurn.addScore : -1)
              ),
              Expanded(flex: 1, child:
                PlayerList(playerName: 'Player 1')
              ),
              Expanded(flex: 4, child:
                Board()
              ),
              Expanded(flex: 1, child:
                ScoreResult(playerName: 'Player 2',
                  totalPlayerScore: state.currentBoard.totalScorePlayer2,
                  addPlayerScore: state.currentBoard.lastTurn.player == 2 ?
                  state.currentBoard.lastTurn.addScore : -1)
              ),
              Expanded(flex: 1, child:
                PlayerList(playerName: 'Player 2')
              ),
            ],
          ),
        )
      );
      }
      )
    );
  }
}