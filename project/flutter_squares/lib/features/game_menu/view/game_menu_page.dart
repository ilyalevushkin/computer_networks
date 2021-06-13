import 'package:flutter/material.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_squares/features/game_menu/bloc/game_menu_bloc.dart';

class GameMenuPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final theme = context.read<ITheme>();
    return BlocProvider(
      create: (context) => GameMenuBloc(),
      child: Container(
      ),
    );
  }
}