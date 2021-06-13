part of 'auth_bloc.dart';

enum AuthStatus {
  unknown,
  authenticated,
  unauthenticated,
  failure,
}

class AuthState extends Equatable {
  const AuthState._({
    this.status = AuthStatus.unknown,
    this.token = '',
    this.failure = '',
  });

  const AuthState.unknown() : this._();

  const AuthState.authenticated(String token)
      : this._(status: AuthStatus.authenticated, token: token);

  const AuthState.unauthenticated()
      : this._(status: AuthStatus.unauthenticated);

  const AuthState.failure(String failure)
      : this._(status: AuthStatus.failure, failure: failure);

  final AuthStatus status;
  final String token;
  final String failure;

  @override
  List<Object> get props => [status, token];
}
