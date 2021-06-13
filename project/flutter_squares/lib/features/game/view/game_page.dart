import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_squares/features/game/bloc/game_bloc.dart';
import 'package:flutter_squares/features/game/view/board.dart';
import 'package:flutter_squares/features/game/view/player_list.dart';

class GamePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final theme = context.read<ITheme>();
    return BlocProvider(
      create: (context) => GameBloc(),
      child: Align(alignment: Alignment.topCenter,
      child: Container(
        child: Row(
          children: [
            PlayerList(player: 'Player 1'),
            Board(),
            PlayerList(player: 'Player 2')
          ],
        ),
      )
      )
    );
  }
}