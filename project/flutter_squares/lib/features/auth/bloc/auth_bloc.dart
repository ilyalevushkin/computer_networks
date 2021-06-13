import 'dart:async';

import 'package:flutter_squares/core/domain/repos/auth/auth_repo.dart';
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:shared_preferences/shared_preferences.dart';

part 'auth_event.dart';
part 'auth_state.dart';

// Следит за текущим состоянием авторизации.
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  AuthBloc({
    required AuthRepo authRepo,
  })   : _authRepo = authRepo,
        super(const AuthState.unknown()) {
    (() async {
      // Ищем токен в хранилище и ставим, если нашелся.
      final instance = await SharedPreferences.getInstance();
      final token = instance.getString(_authRepo.tokenKey);
      if (token != null) {
        _authRepo.setToken(token);
        authenticated(token);
      } else {
        unauthenticated();
      }
    })();
  }

  final AuthRepo _authRepo;

  void unauthenticated() {
    add(AuthUnauthenticated());
  }

  void authenticated(String token) {
    add(AuthAuthenticated(token));
  }

  void requestSignout() {
    add(AuthSignoutRequested());
  }

  void requestSignin(String phoneNumber, String password) {
    add(AuthSigninRequested(phoneNumber, password));
  }

  @override
  Stream<AuthState> mapEventToState(
    AuthEvent event,
  ) async* {
    if (event is AuthSignoutRequested) {
      yield await _mapAuthSignoutRequested(event);
    } else if (event is AuthUnauthenticated) {
      yield AuthState.unauthenticated();
    } else if (event is AuthAuthenticated) {
      yield await _mapAuthAuthenticated(event);
    } else if (event is AuthSigninRequested) {
      yield await _mapAuthSigninRequested(event);
    }
  }

  Future<AuthState> _mapAuthSigninRequested(AuthSigninRequested event) async {
    final instance = await SharedPreferences.getInstance();
    return await _authRepo
        .signIn(username: event.phoneNumber, password: event.password)
        .then((result) {
      final token = result.value;
      if (token == null) {
        return AuthState.failure(result.error?.reason ?? 'Unknown failure');
      } else {
        instance.setString(_authRepo.tokenKey, token);
        return AuthState.authenticated(token);
      }
    }, onError: (_) {
      return AuthState.unknown();
    });
  }

  Future<AuthState> _mapAuthAuthenticated(AuthAuthenticated event) async {
    final instance = await SharedPreferences.getInstance();
    instance.setString(_authRepo.tokenKey, event.token);
    return AuthState.authenticated(event.token);
  }

  Future<AuthState> _mapAuthSignoutRequested(AuthSignoutRequested event) async {
    final instance = await SharedPreferences.getInstance();
    instance.remove(_authRepo.tokenKey);
    return await _authRepo.signOut().then((result) {
      return result.error == null
          ? AuthState.unauthenticated()
          : AuthState.unknown();
    }, onError: (_) {
      return AuthState.unknown();
    });
  }
}
