import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_squares/features/game/bloc/game_bloc.dart';
import 'package:flutter_squares/features/game/widgets/widgets.dart';


class Board extends StatefulWidget {
  @override
  _BoardState createState() => _BoardState();
}

class _BoardState extends State<Board> {
  @override
  Widget build(BuildContext context) {
    final theme = context.read<ITheme>();
    return BlocBuilder<GameBloc, GameState>(
        builder: (context, state) {
          return Column(
            children: [
              ScoreResults(),
              Text('here is the board'),
            ],
          );
        }
    );
  }
}