import 'dart:async';
import 'package:flutter_squares/core/domain/repos/result.dart';

import 'auth_repo.dart';

class UserAuthenticationRepository implements AuthRepo {
  //final ApiClient _api;
  //final UsersApi _uApi;

  @override
  Future<Result<String>> signIn({
    required String username,
    required String password,
  }) async {
    return Ok('OK');
  }

  @override
  Future<Result<void>> signOut() async {
    return Result();
  }

  @override
  Future<Result<void>> setToken(String token) async {
    return Result();
  }

  @override
  Future<Result<int>> currentId() async {
    return Ok(1);
  }

  String get tokenKey => "Squares User Auth token";
}