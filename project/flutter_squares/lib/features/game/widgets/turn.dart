import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_squares/features/game/bloc/game_bloc.dart';
import 'package:flutter_squares/features/game/models/turn.dart';


class TurnCard extends StatelessWidget {

  final Turn turn;

  TurnCard({required this.turn});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<GameBloc, GameState>(
      //buildWhen: (previous, current) => previous.status != current.status,
      builder: (context, state) {
        final theme = context.read<ITheme>();
        return Container(
            width: 50,
            height: 30,
            //decoration: theme.dishListTheme.dishCategoryDecoration,
            //margin: theme.dishListTheme.dishCategoryMargin,
            child: TextButton(
              child: Text(
                this.turn.id.toString(),
                //style: theme.dishListTheme.textStyleCategoryName,
              ),
              onPressed: () {
              },
            ));
      },
    );
  }

}