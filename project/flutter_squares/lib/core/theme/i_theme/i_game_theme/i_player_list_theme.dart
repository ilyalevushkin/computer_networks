part of '../i_theme.dart';

abstract class IPlayerListTheme {
  BoxDecoration turnCardDecoration(bool isLastTurn, bool isCardSelected);

  Color get turnCardColor;

  Color get lastTurnCardColor;

  Color get iconTurnCardColor;

  Color get lastIconTurnCardColor;
}