import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';

part 'light_app_bar_theme.dart';

class LightTheme implements ITheme {
  static LightAppBarTheme _appBarTheme = LightAppBarTheme();

  @override
  IAppBarTheme get appBarTheme => _appBarTheme;
}