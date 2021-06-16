import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_squares/features/game/bloc/game_bloc.dart';
import 'package:flutter_squares/features/game/models/turn.dart';


class TurnCard extends StatelessWidget {

  final Turn turn;
  final int lastTurnId;
  final int boardLastTurnId;
  final AnimationController controller;

  TurnCard({required this.turn, required this.lastTurnId,
  required this.boardLastTurnId, required this.controller});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<GameBloc, GameState>(
      //buildWhen: (previous, current) => previous.status != current.status,
      builder: (context, state) {
        final theme = context.read<ITheme>();
        return Container(
            width: 100,
            margin: EdgeInsets.only(left: 16),
            decoration: theme.playerListTheme.turnCardDecoration(
                this.lastTurnId == this.turn.id,
                this.turn.id == this.boardLastTurnId),
            //margin: theme.dishListTheme.dishCategoryMargin,
            child: TextButton(
              child: Text(
                '+${this.turn.addScore.toString()}',
                style: TextStyle(
                  color: this.lastTurnId == this.turn.id ?
                  theme.playerListTheme.lastIconTurnCardColor :
                  theme.playerListTheme.iconTurnCardColor
                ),
                //style: theme.dishListTheme.textStyleCategoryName,
              ),
              onPressed: () {
                context.read<GameBloc>()
                    .add(SwitchBoard(this.turn.id));
                controller.reset();
                controller.forward();
              },
            ));
      },
    );
  }

}