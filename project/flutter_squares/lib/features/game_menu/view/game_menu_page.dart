import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_squares/features/game/view/game_page.dart';
import 'package:flutter_squares/features/game_menu/bloc/game_menu_bloc.dart';
import 'package:flutter_squares/widgets/squares_scaffold.dart';

class GameMenuPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final theme = context.read<ITheme>();
    return BlocProvider(
      create: (context) => GameMenuBloc(),
      child: Align(
          alignment: Alignment.topCenter,
        child: Container(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              TextButton(
                key: const Key('game_raisedButton'),
                child: Text(
                  'Начать новую игру',
                ),
                onPressed: () {
                  Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => PageView(children: [
                          SquaresScaffold(body: GamePage()),
                        ],),
                      )
                  );
                },
              ),
              TextButton(
                key: const Key('useless_raisedButton'),
                child: Text(
                  'Бесполезная кнопка',
                ),
                onPressed: () {},
              )
          ],),
        )
      )
    );
  }
}