part of 'light_theme.dart';

const Color _yellow = Color.fromRGBO(251, 187, 0, 1);
const Color _orange = Color.fromRGBO(248, 113, 34, 1);
const Color _darkPink = Color.fromRGBO(0xB6, 0x0F, 0x6D, 1);
const Color _purple = Color.fromRGBO(65, 14, 130, 1);
const String _primaryFontFamily = "Roboto";

class LightAppBarTheme implements IAppBarTheme {
  double get height => 100;
  Color get background => _yellow;
  Color get foreground => _purple;

  @override
  TextStyle get titleTextStyle => TextStyle(
      color: foreground,
      fontFamily: _primaryFontFamily,
      fontWeight: FontWeight.w700,
      fontSize: 26);

  @override
  TextStyle get subtitleTextStyle => TextStyle(
      color: foreground,
      fontFamily: _primaryFontFamily,
      fontWeight: FontWeight.w700,
      fontSize: 16);

  AppBarTheme get flutter => AppBarTheme(
      brightness: Brightness.light,
      backgroundColor: background,
      foregroundColor: foreground,
      titleTextStyle: titleTextStyle);
}
