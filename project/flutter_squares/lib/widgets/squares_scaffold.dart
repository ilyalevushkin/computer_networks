import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter/material.dart';
import 'package:flutter_squares/features/auth/bloc/auth_bloc.dart';

class SquaresScaffold extends StatelessWidget {
  final Widget _body;

  SquaresScaffold({Key? key, required Widget body})
      : _body = body,
        super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = context.read<ITheme>();
    final appBarTheme = theme.appBarTheme;
    final bloc = context.read<AuthBloc>();
    return Scaffold(
      appBar: AppBar(
          actions: bloc.state.status == AuthStatus.authenticated
          ? [
          IconButton(
              iconSize: 36,
              color: appBarTheme.foreground,
              onPressed: () {
                bloc.requestSignout();
              },
              icon: Icon(Icons.logout))
          ]
              : [],
          backgroundColor: appBarTheme.background,
          foregroundColor: appBarTheme.foreground,
          titleTextStyle: appBarTheme.titleTextStyle,
          toolbarHeight: appBarTheme.height,
          title: Container(
            child: Column(
              children: [
                Container(),
                Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    'Squares App',
                    style: appBarTheme.titleTextStyle,
                  ),
                ),
              ],
            ),
          )),
      body: _body,
    );
  }
}
