import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {ActivatedRoute, Router} from "@angular/router";
import {AuthenticationService} from "../../services/auth/authentication.service";
import {FriendService} from "../../services/friend/friend.service";
import {first} from "rxjs/operators";
import {GameService} from "../../services/game/game.service";

@Component({
  selector: 'app-game-settings',
  templateUrl: './game-settings.component.html',
  styleUrls: ['./game-settings.component.scss']
})
export class GameSettingsComponent implements OnInit {

  gameForm!: FormGroup;
  loading = false;
  submitted = false;
  returnUrl!: string;
  error = '';

  constructor(private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService,
              private gameService: GameService,
              private friendService: FriendService) {

  }

  ngOnInit(): void {
    this.gameForm = this.formBuilder.group({
            turn: ['', Validators.required],
            rows: ['', Validators.required],
            columns: ['', Validators.required]
        });

        // get return url from route parameters or default to 'profile'
        this.returnUrl = '/game';
  }

  // convenience getter for easy access to form fields
    get f() { return this.gameForm.controls; }

    create_table(rows: number, columns: number): string {
    let str = '';
    for (let i = 0; i < rows * columns; i++)
    {
      str += '0';
    }
    return str;
    }

    onSubmit() {
        this.submitted = true;

        // stop here if form is invalid
        if (this.gameForm.invalid) {
            return;
        }

        this.loading = true;
        let game: any = JSON.stringify({Game: {
              player_1_id: this.friendService.friend_info.id,
              player_2_id: this.authenticationService.currentUserValue.id,
              game_state: {
                turn: this.f.turn.value == "me"? '2': '1',
                columns: this.f.columns.value,
                rows: this.f.rows.value,
                table_with_chips: this.create_table(this.f.rows.value, this.f.columns.value)
              }
            }});
        this.gameService.createGame(game).subscribe(
                game_full_info => {
                    this.gameService.setGameToLocalStorage(game_full_info.Game!);
                    this.router.navigate([this.returnUrl]);
                },
                error => {
                    this.error = error;
                    this.loading = false;
                    console.log(this.error);
                });
    }

}
