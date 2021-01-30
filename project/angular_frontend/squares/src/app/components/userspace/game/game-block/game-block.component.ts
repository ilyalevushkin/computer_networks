import {Component, Input, OnInit, Output, EventEmitter} from '@angular/core';
import {Game_full_info} from "../../../../models/dto/game";
import {Router} from "@angular/router";
import {AuthenticationService} from "../../../../services/auth/authentication.service";
import {GameService} from "../../../../services/game/game.service";

@Component({
  selector: 'app-game-block',
  templateUrl: './game-block.component.html',
  styleUrls: ['./game-block.component.scss']
})
export class GameBlockComponent implements OnInit {

  @Input() public cur_game!: Game_full_info;
  @Output() curGameChange = new EventEmitter<Game_full_info>();

  public error = '';

  constructor(private router: Router,
              private authenticationService: AuthenticationService,
              private gameService: GameService) { }

  ngOnInit(): void {
  }

  cellSelect(pos: number, columns: number, rows: number) {
    const row_pos = Math.floor(pos / columns);
    const column_pos = pos - row_pos * columns;
    const value = (this.cur_game?.player_1?.id == this.authenticationService.currentUserValue.id) ? '1': '2';
    console.log(row_pos, column_pos, value);
    this.gameService.patchGame(this.cur_game?.id!, {'Game_state_update':{
      'column_pos': column_pos,
      'row_pos': row_pos,
      'value': value
    }}).subscribe(
      game => {
        if (game.Game) {
          this.cur_game = game.Game;
          this.curGameChange.emit(game.Game);
        }
      },
      error => {
          this.error = error;
          console.log(this.error);
        }
    );
  }

  not_my_turn(): boolean {
    const turn = this.cur_game?.game_state?.turn;
    return (((this.cur_game?.player_1?.id == this.authenticationService.currentUserValue.id) &&
          (turn == '2')) || ((this.cur_game?.player_2?.id == this.authenticationService.currentUserValue.id) &&
          (turn == '1')));
  }

  get_percent_length(elems_count: number): string {
    let res = 100 / elems_count;
    return res + "%";
  }

  is_cell_bright(pos: number, columns: number): boolean {
    const row_pos = Math.floor(pos / columns);
    const columns_pos = pos - row_pos * columns;
    let value = false;
    if (row_pos % 2 == 0) {
      value = !value;
      if (columns_pos % 2 == 0) {
        value = !value;
      }
    }
    else {
      if (columns_pos % 2 == 0) {
        value = !value;
      }
      if (columns % 2 == 0) {
        value = !value;
      }
    }
    return value;
  }

}
