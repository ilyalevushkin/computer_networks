part of '../light_theme.dart';

class LightPlayerListTheme implements IPlayerListTheme {
  @override
  BoxDecoration turnCardDecoration(bool isLastTurn, bool isCardSelected) =>
      BoxDecoration(
      color: isLastTurn ? lastTurnCardColor : turnCardColor,
      borderRadius: BorderRadius.circular(isCardSelected ? 54.0 : 18.0));

  @override
  Color get turnCardColor => _grey2;

  @override
  Color get lastTurnCardColor => _grey3;

  @override
  Color get iconTurnCardColor => _white2;

  @override
  Color get lastIconTurnCardColor => _white3;
}