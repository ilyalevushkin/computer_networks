part of '../light_theme.dart';

class LightGameResultsTheme implements IGameResultsTheme {
  TextStyle get playerNameTextStyle => TextStyle(
      color: Colors.black,
      fontFamily: fontFamilyTextTheme,
      fontWeight: FontWeight.bold,
      fontSize: 40);
}