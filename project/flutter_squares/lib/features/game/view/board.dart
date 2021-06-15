import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_squares/features/game/bloc/game_bloc.dart';
import 'package:flutter_squares/features/game/models/models.dart';
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
        //buildWhen: (previous, current) => previous.currentBoard != current.currentBoard,
        builder: (context, state) {
          return Container(
                  clipBehavior : Clip.antiAlias,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(8.0)
                  ),
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

                    bool isLastPressed = (rowPos == state.currentBoard.lastTurn.rowPos) &&
                        (columnPos == state.currentBoard.lastTurn.columnPos) &&
                        (rowPos == state.currentBoard.lastTurn.rowPos);
                    double opacity = isLastPressed ? 0.25 : 1;

                    return Container(
                      child: RawMaterialButton(
                        child: (pressedBySb != 0) ? Icon(
                          Icons.circle,
                          color: pressedBySb == 1 ? Colors.black : Colors.white,
                        ) : null,
                        onPressed: (pressedBySb == 0) && (state.currentBoard.enabled)
                            ? () {
                          context.read<GameBloc>().add(TurnMade(rowPos, columnPos));
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