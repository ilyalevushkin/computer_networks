import { Injectable } from '@angular/core';
import {environment} from "../../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {Game, Game_state_update, Get_games} from "../../models/dto/game";
import {Friendship, Get_friends, Patch_friends_friendid, Post_friends} from "../../models/dto/friend";
import {User} from "../../models/dto/user";

@Injectable({
  providedIn: 'root'
})
export class FriendService {

  private url = `${environment.baseUrl}/api/v1/friends`;

  friend_info: User = {id : 0,
                      user:{
                        username: "no_info",
                        first_name: "no_info",
                        last_name: "no_info",
                        email: "no_info"
                      },
                      phone: "no_info",
                      about: "no_info",
                      photo: "/media/users/photo/base_photo.jpg"};

  is_already_friend: boolean = false;
  is_already_invited: boolean = false;

  constructor(private http: HttpClient) { }

  public getFriends(reverse: boolean): Observable<Get_friends> {
        return !reverse ? this.http.get(`${this.url}`): this.http.get(`${this.url}?reverse=True`);
    }

    public getFriend(id: number): Observable<Friendship> {
        return this.http.get(`${this.url}/${id}`);
    }

    public createFriendship(source: Post_friends): Observable<any> {
        return this.http.post(`${this.url}`, source);
    }

    public deleteFriendship(id: number): Observable<any> {
        return this.http.delete(`${this.url}/${id}`);
  }

    public patchFriendship(id: number, source: Patch_friends_friendid): Observable<Friendship> {
      return this.http.patch(`${this.url}/${id}`, source);
    }

}
