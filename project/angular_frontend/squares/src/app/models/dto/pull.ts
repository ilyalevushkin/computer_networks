import {User} from "./user";

export interface Player {
  player?: User;
  date_time_appear?: string;
}

export interface Get_pull_players {
  Pull_players?:Player[];
}
