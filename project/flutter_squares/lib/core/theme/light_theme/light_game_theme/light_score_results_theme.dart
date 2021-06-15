part of '../light_theme.dart';

class LightScoreResultsTheme implements IScoreResultsTheme {
  Color get playerNameColor => _white;
  Color get scoreColor => _white2;

  TextStyle get playerNameTextStyle => TextStyle(
      color: playerNameColor,
      fontFamily: fontFamilyTextTheme,
      fontWeight: FontWeight.normal,
      fontSize: 20);

  TextStyle get totalScoreTextStyle => TextStyle(
      color: scoreColor,
      fontFamily: fontFamilyTextTheme,
      fontWeight: FontWeight.normal,
      fontSize: 20);

  TextStyle get addScoreTextStyle => TextStyle(
      color: scoreColor,
      fontFamily: fontFamilyTextTheme,
      fontWeight: FontWeight.bold,
      fontSize: 30);
}