import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_squares/features/game/bloc/game_bloc.dart';
import 'package:flutter_squares/features/game/view/board.dart';
import 'package:flutter_squares/features/game/view/player_list.dart';
import 'package:flutter_squares/features/game/widgets/score_results.dart';

import 'game_results.dart';

class GamePage extends StatefulWidget {
  @override
  _GamePageState createState() => _GamePageState();
}

class _GamePageState extends State<GamePage> with SingleTickerProviderStateMixin {

  late Animation animation;
  late AnimationController controller;

  @override
  void initState() {
    super.initState();
    controller = AnimationController(vsync: this,
        duration: Duration(seconds: 1));

    TweenSequence<double> tweenSequence = TweenSequence<double>(
      <TweenSequenceItem<double>>[
        TweenSequenceItem<double>(
          tween: Tween<double>(begin: 1.0, end: 0.2)
              .chain(CurveTween(curve: Curves.easeIn)),
          weight: 50.0,
        ),
        TweenSequenceItem<double>(
          tween: Tween<double>(begin: 0.2, end: 1.0)
              .chain(CurveTween(curve: Curves.easeIn)),
          weight: 50.0,
        ),
        TweenSequenceItem<double>(
          tween: Tween<double>(begin: 1.0, end: 0.2)
              .chain(CurveTween(curve: Curves.easeIn)),
          weight: 50.0,
        ),
        TweenSequenceItem<double>(
          tween: Tween<double>(begin: 0.2, end: 1.0)
              .chain(CurveTween(curve: Curves.easeIn)),
          weight: 50.0,
        ),
      ],
    );
    animation = tweenSequence.animate(controller);
    animation.addListener(() {
      setState(() {
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = context.read<ITheme>();
    return BlocProvider(
      create: (context) => GameBloc(),
      child: BlocBuilder<GameBloc, GameState>(
      builder: (context, state) {
        Widget game = Align(alignment: Alignment.topCenter,
        child: Container(
          decoration: BoxDecoration(
            color: theme.gamePageTheme.backgroundColor
          ),
          child: Column(
            children: [
              Expanded(flex: 2, child:
                ScoreResult(playerName: 'Player 1',
                  totalPlayerScore: state.currentBoard.totalScorePlayer1,
                  addPlayerScore: state.currentBoard.lastTurn.player == 1 ?
                  state.currentBoard.lastTurn.addScore : -1)
              ),
              Expanded(flex: 2, child:
                PlayerList(playerName: 'Player 1', controller: controller,)
              ),
              Expanded(flex: 9, child:
                Board(controller: controller, animation: animation,)
              ),
              Expanded(flex: 2, child:
                ScoreResult(playerName: 'Player 2',
                  totalPlayerScore: state.currentBoard.totalScorePlayer2,
                  addPlayerScore: state.currentBoard.lastTurn.player == 2 ?
                  state.currentBoard.lastTurn.addScore : -1)
              ),
              Expanded(flex: 2, child:
                PlayerList(playerName: 'Player 2', controller: controller,)
              ),
            ],
          ),
        )
      );
        if (state.currentBoard.isFull) {
          return Stack(
            alignment: AlignmentDirectional.center,
            textDirection: TextDirection.ltr,
            children: [game,
              GameResults(scorePlayer1: state.currentBoard.totalScorePlayer1,
                  scorePlayer2: state.currentBoard.totalScorePlayer2)
            ],
          );
        }
        else {
          return game;
        }
      }
      )
    );
  }
}