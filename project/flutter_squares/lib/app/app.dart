import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter/services.dart';

import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';
import 'package:flutter_squares/core/theme/light_theme/light_theme.dart';
import 'package:flutter_squares/core/domain/repos/auth/auth_repo.dart';
import 'package:flutter_squares/core/domain/repos/auth/user_auth_repo.dart';
import 'package:flutter_squares/features/auth/bloc/auth_bloc.dart';
import 'pages/pages.dart';

void runUserApp() async {
  //final api = ApiClient(basePathOverride: r'http://161.35.217.187:9001/api/v1');
  runApp(MultiRepositoryProvider(providers: [
    RepositoryProvider<ITheme>.value(
      value: LightTheme(),
    ),
    RepositoryProvider<AuthRepo>.value(
      value: UserAuthenticationRepository(),
    ),
  ],
      child: App()));
}

class App extends StatelessWidget {
  const App({
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
    ]);
    SystemChrome.setEnabledSystemUIOverlays([]);
    return BlocProvider(
      create: (context) => AuthBloc(
        authRepo: RepositoryProvider.of(context),
      ),
      child: AppView(),
    );
  }
}

class AppView extends StatefulWidget {
  @override
  _AppViewState createState() => _AppViewState();
}

class _AppViewState extends State<AppView> {
  final _navigatorKey = GlobalKey<NavigatorState>();

  NavigatorState get _navigator => _navigatorKey.currentState!;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      navigatorKey: _navigatorKey,
      debugShowCheckedModeBanner: false,
      builder: (context, child) {
        return BlocListener<AuthBloc, AuthState>(
          listenWhen: (previous, current) =>
          current.status == AuthStatus.authenticated ||
              current.status == AuthStatus.unauthenticated,
          listener: (context, state) async {
            switch (state.status) {
              case AuthStatus.authenticated:
                _navigator.pushAndRemoveUntil<void>(
                  HomePage.route(),
                      (route) => false,
                );
                break;
              case AuthStatus.unauthenticated:
                _navigator.pushAndRemoveUntil<void>(
                  HomePage.route(),
                      (route) => false,
                );
                break;
              default:
                break;
            }
          },
          child: child,
        );
      },
      onGenerateRoute: (_) => SplashPage.route(),
    );
  }
}