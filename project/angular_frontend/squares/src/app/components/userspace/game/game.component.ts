import { Component, OnInit } from '@angular/core';
import {AuthenticationService} from "../../../services/auth/authentication.service";
import {Router} from "@angular/router";
import {GameService} from "../../../services/game/game.service";
import {Game_full_info} from "../../../models/dto/game";
import {Observable, timer} from "rxjs";
import {User, User_main} from "../../../models/dto/user";


@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.scss']
})

export class GameComponent implements OnInit {

  my_timer: number = 0;
  opponent_timer: number = 0;

  cur_game: Game_full_info = {
    id: -1,
    player_1: {id : 0,
                user:{
                  username: "no_info",
                  first_name: "no_info",
                  last_name: "no_info",
                  email: "no_info"
                },
                phone: "no_info",
                about: "no_info",
                photo: "/media/users/photo/base_photo.jpg"},
    player_2: {id : 0,
                user:{
                  username: "no_info",
                  first_name: "no_info",
                  last_name: "no_info",
                  email: "no_info"
                },
                phone: "no_info",
                about: "no_info",
                photo: "/media/users/photo/base_photo.jpg"},
    game_state: {
      status: "no_info",
      turn: "no_info",
      player_1_points: "no_info",
      player_2_points: "no_info",
      columns: -1,
      rows: -1,
      table_with_chips: "no_info"
    },
    date_time_from: "no_info",
    date_time_to: "no_info"
  };

  error = '';

  not_my_turn(): boolean {
    const turn = this.cur_game.game_state?.turn;
    return (((this.cur_game.player_1?.id == this.authenticationService.currentUserValue.id) &&
          (turn == '2')) || ((this.cur_game.player_2?.id == this.authenticationService.currentUserValue.id) &&
          (turn == '1')));
  }

  game_refresh()
  {
    this.cur_game = this.gameService.getGameFromLocalStorage();
    if (this.cur_game && this.cur_game?.id !== -1) {
      this.gameService.getGame(this.cur_game?.id!).subscribe(
        game_full_info => {
          if (game_full_info.Game) {
            this.cur_game = game_full_info.Game;
            this.gameService.setGameToLocalStorage(this.cur_game);
          }
        },
        error => {
          this.error = error;
          console.log(this.error);
        });
    }
    else if (!this.cur_game || this.cur_game.id == -1) {
      this.gameService.getActiveGame(this.authenticationService.currentUserValue.id).subscribe(
        game_full_info => {
          if (game_full_info.Game) {
            console.log(game_full_info.Game);
            this.cur_game = game_full_info.Game;
            this.gameService.setGameToLocalStorage(game_full_info.Game);
          }
        },
        error => {
          this.error = error;
          console.log(this.error);
        }
      )
    }
    if (this.cur_game.id && this.cur_game.id !== -1)
    {
      if (this.cur_game.game_state?.status == '-1')
      {
        if (this.not_my_turn())
        {
          timer(3000).subscribe(res => this.game_refresh());
        }
      }
    }
  }

  constructor(private router: Router,
              private authenticationService: AuthenticationService,
              private gameService: GameService) {
    this.cur_game = this.gameService.getGameFromLocalStorage();
  }

  ngOnInit(): void {
    this.game_refresh();
  }

}
