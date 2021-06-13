import 'package:flutter/material.dart';
import 'package:flutter_squares/features/game_menu/view/game_menu_page.dart';
import 'package:flutter_squares/widgets/squares_scaffold.dart';

class HomePage extends StatelessWidget {
  static Route route() {
    return MaterialPageRoute<void>(builder: (_) => HomePage());
  }

  @override
  Widget build(BuildContext context) {
    return PageView(
      children: [
        SquaresScaffold(body: GameMenuPage()),
      ],
    );
  }
}