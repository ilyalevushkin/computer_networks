import { Injectable } from '@angular/core';
import {environment} from "../../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {Get_pull_players, Player} from "../../models/dto/pull";
import {User} from "../../models/dto/user";

@Injectable({
  providedIn: 'root'
})
export class PullService {

  private url = `${environment.baseUrl}/api/v1/pull_players`;

  constructor(private http: HttpClient) { }

  public getPullPlayers(): Observable<Get_pull_players> {
        return this.http.get(`${this.url}`);
  }

  // тут source не нужен вроде бы. требуется только user pk. подумать над этим
  public postPullPlayer(): Observable<any> {
    return this.http.post(`${this.url}`, {'': 0});
  }

  public deletePullPlayer(): Observable<any> {
        return this.http.delete(`${this.url}`);
  }


}
