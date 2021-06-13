import 'dart:async';
import 'package:flutter_squares/core/domain/repos/result.dart';

abstract class AuthRepo {
  Future<Result<String>> signIn({
    required String username,
    required String password,
  });

  Future<Result<void>> signOut();

  Future<Result<void>> setToken(String token);

  Future<Result<int>> currentId();

  String get tokenKey;
}