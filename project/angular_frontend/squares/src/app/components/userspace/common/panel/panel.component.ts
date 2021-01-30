import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {AuthenticationService} from "../../../../services/auth/authentication.service";
import {User, User_main} from "../../../../models/dto/user";
import {first} from "rxjs/operators";
import {UserService} from "../../../../services/user/user.service";


@Component({
  selector: 'app-panel',
  templateUrl: './panel.component.html',
  styleUrls: ['./panel.component.scss']
})
export class PanelComponent implements OnInit {

  public btnPressed = false;
  error = '';

  currentUser!: User_main;

  user_info = {username: "no_info", photo: "/media/users/photo/base_photo.jpg"};

    constructor(
        private router: Router,
        private authenticationService: AuthenticationService,
        private userService: UserService
    ) {
        this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
        this.user_info.username = this.userService.getUserFromLocalStorage().user.username;
        this.user_info.photo = this.userService.getUserFromLocalStorage().photo;
    }

  ngOnInit(): void {
  }

  changeBtnState() {
    this.btnPressed = !this.btnPressed;
  }

    logout() {
        this.userService.getLogoutUser()
            .pipe(first())
            .subscribe(
                data => {
                    this.router.navigate(['logout']);
                    this.authenticationService.logout();
                },
                error => {
                    this.error = error;
                });
    }

}
