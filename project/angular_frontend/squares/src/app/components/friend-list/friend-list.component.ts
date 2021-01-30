import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {AuthenticationService} from "../../services/auth/authentication.service";
import {UserService} from "../../services/user/user.service";
import {FriendService} from "../../services/friend/friend.service";
import {first} from "rxjs/operators";
import {Friendship, Get_friends} from "../../models/dto/friend";

@Component({
  selector: 'app-friend-list',
  templateUrl: './friend-list.component.html',
  styleUrls: ['./friend-list.component.scss']
})
export class FriendListComponent implements OnInit {

  friends!: Get_friends;

  friends_by_me!: Get_friends;

  friends_list!: Get_friends[];

  friend_selected: boolean = false;
  friendship_selected!: Friendship;

  page: number = 0;

  error = '';

  constructor(private router: Router,
        private authenticationService: AuthenticationService,
        private friendService: FriendService) {
    this.friendService.getFriends(false)
            .subscribe(friends => {
                this.friends = friends;
                const friends_length = this.friends.Friends === undefined ? 0 : this.friends.Friends.length;
                let i = 0;
                this.friends_list = [];
                while (i < friends_length)
                {
                  let iter_friends = [];
                  let j = 0;
                  while (j < 9 && i < friends_length)
                  {
                    iter_friends.push(this.friends.Friends![i]);
                    j++;
                    i++;
                  }
                  this.friends_list.push({'Friends': iter_friends});
                }
            },
              error => {
                this.error = error;
              });
    this.friendService.getFriends(true)
            .subscribe(friends_by_me => {
                this.friends_by_me = friends_by_me;
            },
              error => {
                this.error = error;
              });
  }

  friendSelect(friend: Friendship) {
    if (!this.friend_selected || friend.friend?.id == this.friendship_selected.friend?.id)
    {
      this.friend_selected = !this.friend_selected;
    }
    this.friendship_selected = friend;
  }

  showFriendInfo() {
    this.friendService.friend_info = this.friendship_selected.friend || {id : 0,
                      user:{
                        username: "no_info",
                        first_name: "no_info",
                        last_name: "no_info",
                        email: "no_info"
                      },
                      phone: "no_info",
                      about: "no_info",
                      photo: "no_info"};
    this.friendService.is_already_friend = true;
    this.friendService.is_already_invited = this.friendship_selected.status == 'Да';
  }

  getFriendStatus(friend: Friendship): string {
    const friends_by_me_length = this.friends_by_me.Friends === undefined ? 0 : this.friends_by_me.Friends.length;
    for (let i = 0; i < friends_by_me_length; i++) {
      if (friend.friend?.id == this.friends_by_me.Friends![i].user_friend?.id) {
        return this.friends_by_me.Friends![i].status || "Нет";
      }
    }
    return "Нет";
  }

  ngOnInit(): void {
  }

}
