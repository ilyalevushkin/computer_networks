import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { User_main } from '../../models/dto/user';
import {UserService} from "../user/user.service";
import {Post_users_signin} from "../../models/dto/user";

@Injectable({ providedIn: 'root' })
export class AuthenticationService {
    private currentUserSubject: BehaviorSubject<User_main>;
    public currentUser: Observable<User_main>;

    constructor(private http: HttpClient, private userService: UserService) {
        this.currentUserSubject = new BehaviorSubject<User_main>(JSON.parse(
          localStorage.getItem('currentUser') || '{}'));
        this.currentUser = this.currentUserSubject.asObservable();
    }

    public get currentUserValue(): User_main {
        return this.currentUserSubject.value;
    }

    login(source: Post_users_signin) {
        return this.userService.postLoginUser(source)
            .pipe(map(token => {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('currentUser', JSON.stringify(token));
                this.currentUserSubject.next(token);
                return token;
            }));
    }

    logout() {
        // remove user from local storage to log user out
        localStorage.removeItem('currentUser');
        this.currentUserSubject.next(JSON.parse('{}'));
    }
}
