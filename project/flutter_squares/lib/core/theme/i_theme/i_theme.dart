import 'package:flutter/material.dart';
part 'i_app_bar_theme.dart';
part 'i_game_theme/i_board_theme.dart';
part 'i_game_theme/i_player_list_theme.dart';
part 'i_game_theme/i_game_page_theme.dart';
part 'i_game_theme/i_score_results_theme.dart';
part 'i_game_theme/i_game_results_theme.dart';

abstract class ITheme {
  IAppBarTheme get appBarTheme;
  IBoardTheme get boardTheme;
  IPlayerListTheme get playerListTheme;
  IGamePageTheme get gamePageTheme;
  IScoreResultsTheme get scoreResultsTheme;
  IGameResultsTheme get gameResultsTheme;
}