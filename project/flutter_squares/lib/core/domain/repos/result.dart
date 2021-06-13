import 'package:flutter_squares/core/domain/repos/failure.dart';
import 'package:dio/dio.dart';

class Result<T> {
  T? _value;
  Failure? _error;
  Result({T? value, Failure? error})
      : _value = value,
        _error = error;

  Failure? get error => _error;

  T? get value => _value;

  Result<S> to<S>() {
    return Result(error: this.error);
  }

  String toString() {
    return "Result($_value, $_error)";
  }
}

class Ok<T> extends Result<T> {
  Ok(T value) : super(value: value);
}

class Err<T> extends Result<T> {
  Err(Failure error) : super(error: error);
}

Result<T> resultFromResponse<T>(Response<T> response) {
  final code = response.statusCode ?? 1;
  if (code >= 200 && code < 300) {
    final data = response.data;
    if (data != null) {
      return Ok(data);
    } else {
      return Result();
    }
  }
  return Err(failureFromResponse(response));
}

Result<T> resultFromError<T>(dynamic error) {
  if (error is DioError) {
    final response = error.response;
    if (response is Response<T>) {
      return resultFromResponse(response);
    }
  }
  return Err(SimpleFailure(1, error.toString()));
}
