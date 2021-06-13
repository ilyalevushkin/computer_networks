import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_squares/features/game/bloc/game_bloc.dart';


class ScoreResults extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<GameBloc, GameState>(
      //buildWhen: (previous, current) => previous.status != current.status,
      builder: (context, state) {
        final theme = context.read<ITheme>();
        return Container(
            width: 200,
            height: 50,
            //decoration: theme.dishListTheme.dishCategoryDecoration,
            //margin: theme.dishListTheme.dishCategoryMargin,
            child: Row(
              children: [
                Text('Player 1 Score'),
                Text('+ Player 1 Score'),
                Text('Player 2 Score'),
                Text('+ Player 2 Score'),
              ],
            )
        );
      },
    );
  }

}