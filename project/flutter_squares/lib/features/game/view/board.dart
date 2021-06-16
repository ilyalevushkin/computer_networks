import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_squares/features/game/bloc/game_bloc.dart';
import 'package:flutter_squares/features/game/models/models.dart';
import 'package:flutter_squares/features/game/widgets/widgets.dart';


class Board extends StatefulWidget {

  Board({required this.controller,
  required this.animation});

  final AnimationController controller;
  final Animation animation;

  @override
  _BoardState createState() => _BoardState(controller: controller,
  animation: animation);
}

class _BoardState extends State<Board> {

  _BoardState({required this.controller, required this.animation});

  final AnimationController controller;
  final Animation animation;

  bool calcIsLastAddedScore(Map<String, List<int>> addedScoreDotsPos,
  int rowPos, int columnPos) {
    for (int index = 0; index < addedScoreDotsPos['Rows']!.length; index++) {
      if ((rowPos == addedScoreDotsPos['Rows']![index]) &&
          (columnPos == addedScoreDotsPos['Columns']![index])) {
        return true;
      }
    }
    return false;
  }

  @override
  Widget build(BuildContext context) {
    final theme = context.read<ITheme>();
    return BlocBuilder<GameBloc, GameState>(
        //buildWhen: (previous, current) => previous.currentBoard != current.currentBoard,
        builder: (context, state) {
          return Container(
                  child: GridView.builder(
                  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: state.currentBoard.rows,
                    crossAxisSpacing: 0,
                    mainAxisSpacing: 0,
                ),
                  itemCount: state.currentBoard.rows * state.currentBoard.columns,
                  itemBuilder: (BuildContext context, int index) {
                    bool darkColor;
                    int rowPos = index ~/ state.currentBoard.rows;
                    int columnPos = index % state.currentBoard.columns;
                    darkColor = ((rowPos.isEven && columnPos.isOdd) ||
                        (rowPos.isOdd && columnPos.isEven));
                    int pressedBySb = state.currentBoard.board[rowPos][columnPos];

                    /*bool isLastPressed = (rowPos == state.currentBoard.lastTurn.rowPos) &&
                        (columnPos == state.currentBoard.lastTurn.columnPos) &&
                        (rowPos == state.currentBoard.lastTurn.rowPos);*/
                    //double opacity = isLastPressed ? 0.25 : 1;
                    bool isLastAddedScore = calcIsLastAddedScore(
                        state.currentBoard.lastTurn.addedScoreDotsPos,
                    rowPos, columnPos);
                    double opacity = isLastAddedScore ? animation.value : 1;
                    return Container(
                        child: RawMaterialButton(
                          child: (pressedBySb != 0) ? Icon(Icons.circle,
                                    color: pressedBySb == 1 ?
                                    Colors.black : Colors.white) : null,
                          onPressed: (pressedBySb == 0) && (state.currentBoard.enabled)
                              ? () {
                            context.read<GameBloc>().add(TurnMade(rowPos, columnPos));
                            controller.reset();
                            controller.forward();
                          } : null,
                        ),
                        color: darkColor ? Color.fromRGBO(202, 114, 65, opacity) :
                        Color.fromRGBO(238, 222, 192, opacity),
                      );
                  }));
        }
    );
  }
}