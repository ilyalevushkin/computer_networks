import 'dart:async';
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';

part 'game_menu_event.dart';
part 'game_menu_state.dart';

class GameMenuBloc extends Bloc<GameMenuEvent, GameMenuState> {

  GameMenuBloc(): super(GameMenuState());

  @override
  Stream<GameMenuState> mapEventToState(
      GameMenuEvent event,
      ) async* {
    /*if (event is PaymentCardNumberChanged) {
      yield _mapCardNumberChangedToState(event, state);
    }*/
  }
}