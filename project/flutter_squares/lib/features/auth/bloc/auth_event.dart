part of 'auth_bloc.dart';

abstract class AuthEvent extends Equatable {
  const AuthEvent();

  @override
  List<Object> get props => [];
}

class AuthAuthenticated extends AuthEvent {
  final String token;
  AuthAuthenticated(this.token);

  @override
  List<Object> get props => [token];
}

class AuthUnauthenticated extends AuthEvent {}

class AuthSignoutRequested extends AuthEvent {}

class AuthSigninRequested extends AuthEvent {
  final String phoneNumber;
  final String password;
  AuthSigninRequested(this.phoneNumber, this.password);

  @override
  List<Object> get props => [phoneNumber, password];
}
