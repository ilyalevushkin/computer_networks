import { Component, OnInit } from '@angular/core';
import {User} from "../../models/dto/user";
import {Router} from "@angular/router";
import {AuthenticationService} from "../../services/auth/authentication.service";
import {UserService} from "../../services/user/user.service";
import {FileUploadService} from "../../services/file_upload/file-upload.service";
import {first} from "rxjs/operators";
import {FriendService} from "../../services/friend/friend.service";

@Component({
  selector: 'app-friend-profile',
  templateUrl: './friend-profile.component.html',
  styleUrls: ['./friend-profile.component.scss']
})
export class FriendProfileComponent implements OnInit {

  user_info: User = {id : 0,
                      user:{
                        username: "no_info",
                        first_name: "no_info",
                        last_name: "no_info",
                        email: "no_info"
                      },
                      phone: "no_info",
                      about: "no_info",
                      photo: "no_info"};

  is_already_friend: boolean = false;
  is_already_invited: boolean = false;

  error = '';

  constructor(private router: Router,
        private authenticationService: AuthenticationService,
        private friendService: FriendService) {
          this.user_info = friendService.friend_info;
          this.is_already_friend = friendService.is_already_friend;
          this.is_already_invited = friendService.is_already_invited;
  }

  ngOnInit(): void {

  }

  addFriend() {
    this.friendService.createFriendship({'Friendship': {'id': this.user_info.id, 'status': 'Нет'}})
            .subscribe(friendship => {
              this.is_already_friend = true;
              this.is_already_invited = false;
            },
              error => {
                this.error = error;
              });
  }

  deleteFriend() {
    this.friendService.deleteFriendship(this.user_info.id!)
            .subscribe(friendship => {
              this.is_already_friend = false;
              this.is_already_invited = false;
            },
              error => {
                this.error = error;
              });
  }

  inviteFriend(invite: boolean) {
    this.friendService.patchFriendship(this.user_info.id!, {'Status': {'ready_to_play': invite}})
            .subscribe(friendship => {
              this.is_already_friend = true;
              this.is_already_invited = invite;
            },
              error => {
                this.error = error;
              });
  }

}
