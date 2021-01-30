import { Injectable } from '@angular/core';
import {environment} from "../../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {Game, Game_full_info, Game_post, Game_state_update, Get_game, Get_games} from "../../models/dto/game";
import {User} from "../../models/dto/user";

@Injectable({
  providedIn: 'root'
})
export class GameService {

  private url = `${environment.baseUrl}/api/v1/games`;

  constructor(private http: HttpClient) { }

  public setGameToLocalStorage(source: Game_full_info) {
    localStorage.setItem('Game_full_info', JSON.stringify(source));
  }

  public getGameFromLocalStorage(): Game_full_info {
    let game_full_info = localStorage.getItem('Game_full_info') || '{}';
    if (game_full_info !== '{}')
    {
      return JSON.parse(game_full_info).Game;
    }
    return JSON.parse(game_full_info);
  }

    public getGames(): Observable<Get_games> {
        return this.http.get(`${this.url}`);
    }

    public getGame(id: number): Observable<Get_game> {
        return this.http.get(`${this.url}/${id}`);
    }

    public getActiveGame(user_id: number): Observable<Get_game> {
      return this.http.get(`${this.url}/users/${user_id}?active=1`)
    }

    public createGame(source: Game_post): Observable<Get_game> {
        return this.http.post(`${this.url}`, source);
    }

    public deleteGame(id: number): Observable<any> {
        return this.http.delete(`${this.url}/${id}`);
  }

    public patchGame(id: number, source: Game_state_update): Observable<Get_game> {
      return this.http.patch(`${this.url}/${id}`, source);
    }

}
