import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {ActivatedRoute, Router} from "@angular/router";
import {AuthenticationService} from "../../services/auth/authentication.service";
import {first} from "rxjs/operators";
import {Post_users_signup} from "../../models/dto/user";
import {UserService} from "../../services/user/user.service";

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {

  registerForm!: FormGroup;
    loading = false;
    submitted = false;
    returnUrl!: string;
    error = '';

    constructor(
        private formBuilder: FormBuilder,
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService,
        private userService: UserService
    ) {
        // redirect to game if already logged in
        if (JSON.stringify(this.authenticationService.currentUserValue) !== '{}') {
            this.router.navigate(['game']);
        }
    }

    ngOnInit() {
        this.registerForm = this.formBuilder.group({
            username: ['', Validators.required],
            email: ['', Validators.required],
            phone: ['', Validators.required],
            password: ['', Validators.required],
            repeat_password: ['', Validators.required]
        });

        // get return url from route parameters or default to 'profile'
        this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || 'login';
    }

    // convenience getter for easy access to form fields
    get f() { return this.registerForm.controls; }

    onSubmit() {
        this.submitted = true;

        // stop here if form is invalid
        if (this.registerForm.invalid) {
            return;
        }

        this.loading = true;
        let register: any = JSON.stringify({User: {user:{
              username: this.f.username.value,
              email: this.f.email.value,
              password: this.f.password.value
            },
            phone: this.f.phone.value,
          }});
        console.log(register);
        this.userService.createUser(register)
            .pipe(first())
            .subscribe(
                data => {
                    this.router.navigate([this.returnUrl]);
                },
                error => {
                    this.error = error;
                    this.loading = false;
                });
    }

}
