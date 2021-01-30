import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {AuthenticationService} from "../../services/auth/authentication.service";
import {UserService} from "../../services/user/user.service";
import {User} from "../../models/dto/user";
import {first, map} from "rxjs/operators";
import {FileUploadService} from "../../services/file_upload/file-upload.service";

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {

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

  error = '';

  edit_mode: boolean = false;

  constructor(private router: Router,
        private authenticationService: AuthenticationService,
        private userService: UserService,
              private fileUploadService: FileUploadService) {
          this.userService.getUser(this.authenticationService.currentUserValue.id!)
            .subscribe(user => {
                this.userService.setUserToLocalStorage(user);
                this.edit_mode = false;
                this.user_info = this.userService.getUserFromLocalStorage();
            },
              error => {
                this.error = error;
              });
  }

  ngOnInit(): void {

  }

  changePhoto(event: any) {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      const formData = new FormData();
      formData.append('file', file);
      this.fileUploadService.upload(formData).subscribe(photo_path => {
        this.user_info.photo = photo_path.file;
        this.userService.setUserToLocalStorage(this.user_info);
        },
        error => {
          this.error = error;
        }
      );
    }
  }

  save_all() {
    this.userService.patchUser(this.user_info.id!, {User_update: {
      user: this.user_info.user,
        phone: this.user_info.phone,
        about: this.user_info.about,
        photo: this.user_info.photo
      }})
            .pipe(first())
            .subscribe(user_update => {
                this.userService.setUserToLocalStorage(user_update.User_update);
                this.edit_mode = false;
            },
              error => {
                this.error = error;
              });
  }

}
