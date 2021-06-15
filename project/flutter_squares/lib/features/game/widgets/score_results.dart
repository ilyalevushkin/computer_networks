import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_squares/features/game/bloc/game_bloc.dart';


class ScoreResult extends StatelessWidget {

  ScoreResult({required this.playerName,
  required this.totalPlayerScore,
  required this.addPlayerScore});

  final String playerName;
  final int totalPlayerScore;
  final int addPlayerScore;

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<GameBloc, GameState>(
      //buildWhen: (previous, current) => previous.status != current.status,
      builder: (context, state) {
        final theme = context.read<ITheme>();
        return Container(
            child: Row(
              children: [
                Expanded(flex: 3, child: Container(
                    margin: EdgeInsets.only(left: 8),
                    child: Icon(
                    Icons.account_box,
                    color: theme.scoreResultsTheme.playerNameColor,
                      size: 40,
                ))),
                Expanded(flex: 4, child: Container(
                    child: Text(playerName,
                  style: theme.scoreResultsTheme.playerNameTextStyle,))),
                Expanded(flex: 3, child:
                Container(child: Icon(
                  Icons.circle,
                  color: playerName == 'Player 1' ? Colors.black : Colors.white,
                ),)
                ),
                Expanded(flex: 7, child: Container(
                    child: Text('Total score $totalPlayerScore',
                  style: theme.scoreResultsTheme.totalScoreTextStyle,))),
                Expanded(flex: 3, child: Container(
                    child: Text(addPlayerScore != -1 ? '+$addPlayerScore' : '',
                  style: theme.scoreResultsTheme.addScoreTextStyle,)))
              ],)
        );
      },
    );
  }

}