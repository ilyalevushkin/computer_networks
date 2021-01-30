import { Injectable } from '@angular/core';
import {environment} from "../../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {BehaviorSubject, Observable} from 'rxjs';
import {
  Get_users,
  User,
  Post_users_signup,
  Post_users_signin,
  Patch_Users_userid,
  Get_user, Photo_path, User_main
} from "../../models/dto/user";


@Injectable({
  providedIn: 'root'
})
export class UserService {

  private url = `${environment.baseUrl}/api/v1/users`;

  constructor(private http: HttpClient) {
  }

  public setUserToLocalStorage(source: User) {
    localStorage.setItem('User_info', JSON.stringify(source));
  }

  public getUserFromLocalStorage(): User {
    return JSON.parse(localStorage.getItem('User_info') || '{}').User;
  }

    public getUsers(): Observable<any> {
        return this.http.get(`${this.url}`);
    }

    public getUser(id: number): Observable<any> {
        return this.http.get(`${this.url}/${id}`);
    }

    public getLogoutUser(): Observable<any> {
      return this.http.get(`${this.url}/signout`);
    }

    public createUser(source: Post_users_signup): Observable<any> {
        return this.http.post<any>(`${this.url}/signup`, source);
    }

    public postLoginUser(source: Post_users_signin): Observable<any> {
      return this.http.post<any>(`${this.url}/signin`, source);
    }

    public patchUser(id: number, source: Patch_Users_userid): Observable<any> {
      return this.http.patch(`${this.url}/${id}`, source);
    }

}
