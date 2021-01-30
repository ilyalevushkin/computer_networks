import { Component, OnInit } from '@angular/core';
import {Get_pull_players, Player} from "../../../models/dto/pull";
import {PullService} from "../../../services/pull/pull.service";
import {Router} from "@angular/router";
import {AuthenticationService} from "../../../services/auth/authentication.service";
import {FriendService} from "../../../services/friend/friend.service";
import {Friendship} from "../../../models/dto/friend";

@Component({
  selector: 'app-pull',
  templateUrl: './pull.component.html',
  styleUrls: ['./pull.component.scss']
})

export class PullComponent implements OnInit {

  public pull_players!: Get_pull_players;

  pull_players_list!: Get_pull_players[];

  self_added: boolean = false;

  player_selected: boolean = false;
  pull_player_selected!: Player;

  page: number = 0;

  error = '';

  constructor(private pullService: PullService,
              private router: Router,
              private authenticationService: AuthenticationService,
              private friendService: FriendService) {
    if (!friendService.friend_info.user.username || friendService.friend_info.user.username == "no_info")
    {
      this.router.navigate(['pull']);
    }
    this.pullService.getPullPlayers()
            .subscribe(pull_players => {
                this.pull_players = pull_players;
                const pull_players_length = this.pull_players.Pull_players === undefined ? 0 : this.pull_players.Pull_players.length;
                let i = 0;
                this.pull_players_list = [];
                while (i < pull_players_length)
                {
                  let iter_pull_players = [];
                  let j = 0;
                  while (j < 9 && i < pull_players_length)
                  {
                    if (this.pull_players.Pull_players![i].player?.id == this.authenticationService.currentUserValue.id)
                    {
                      this.self_added = true;
                    }
                    iter_pull_players.push(this.pull_players.Pull_players![i]);
                    j++;
                    i++;
                  }
                  this.pull_players_list.push({'Pull_players': iter_pull_players});
                }

            },
              error => {
                this.error = error;
                console.error('Error: ', this.error);
              });
  }

  ngOnInit() {
  }

  playerSelect(player: Player) {
    if (!this.player_selected || player.player?.id == this.pull_player_selected.player?.id)
    {
      this.player_selected = !this.player_selected;
    }
    this.pull_player_selected = player;
  }

  showPlayerInfo() {
    this.friendService.friend_info = this.pull_player_selected.player || {id : 0,
                      user:{
                        username: "no_info",
                        first_name: "no_info",
                        last_name: "no_info",
                        email: "no_info"
                      },
                      phone: "no_info",
                      about: "no_info",
                      photo: "/media/users/photo/base_photo.jpg"};
    this.friendService.is_already_friend = false;
    this.friendService.is_already_invited = false;
  }

  addSelfToPull(self_add: boolean) {
    this.self_added = self_add;
    if (self_add)
    {
      this.pullService.postPullPlayer().subscribe( result => {
        console.log(result);
      },
      error => {
        this.error = error;
        console.log(error);
      });
    }
    else
    {
      this.pullService.deletePullPlayer().subscribe( result => {
        console.log(result);
      },
      error => {
        this.error = error;
        console.log(error);
      });
    }

  }

  startGame() {
    this.friendService.friend_info = this.pull_player_selected.player || {id : 0,
                      user:{
                        username: "no_info",
                        first_name: "no_info",
                        last_name: "no_info",
                        email: "no_info"
                      },
                      phone: "no_info",
                      about: "no_info",
                      photo: "/media/users/photo/base_photo.jpg"};
     this.router.navigate(['/game_start']);
  }

}
