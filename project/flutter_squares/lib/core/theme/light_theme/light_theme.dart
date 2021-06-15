import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_squares/core/theme/i_theme/i_theme.dart';

part 'light_app_bar_theme.dart';
part 'light_game_theme/light_board_theme.dart';
part 'light_game_theme/light_player_list_theme.dart';
part 'light_game_theme/light_game_page_theme.dart';
part 'light_game_theme/light_score_results_theme.dart';

const Color _white = Color.fromRGBO(136, 135, 133, 1);
const Color _white2 = Color.fromRGBO(191, 190, 186, 1);
const Color _white3 = Color.fromRGBO(255, 255, 255, 1);

const Color _grey = Color.fromRGBO(59, 57, 54, 1);
const Color _grey2 = Color.fromRGBO(73, 71, 69, 1);
const Color _grey3 = Color.fromRGBO(89, 87, 85, 1);

const String fontFamilyTextTheme = "Roboto";


class LightTheme implements ITheme {
  static LightAppBarTheme _appBarTheme = LightAppBarTheme();
  static LightBoardTheme _boardTheme = LightBoardTheme();
  static LightPlayerListTheme _playerListTheme = LightPlayerListTheme();
  static LightGamePageTheme  _gamePageTheme = LightGamePageTheme();
  static LightScoreResultsTheme _scoreResultsTheme = LightScoreResultsTheme();

  @override
  IAppBarTheme get appBarTheme => _appBarTheme;

  @override
  IBoardTheme get boardTheme => _boardTheme;

  @override
  IPlayerListTheme get playerListTheme => _playerListTheme;

  @override
  IGamePageTheme get gamePageTheme => _gamePageTheme;

  @override
  IScoreResultsTheme get scoreResultsTheme => _scoreResultsTheme;

}