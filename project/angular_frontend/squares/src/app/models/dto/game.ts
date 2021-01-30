import {User} from "./user";


export interface Game {
  id?: number;
  player_1_id?: number;
  player_2_id?: number;
  game_state?:{
    status?: string;
    turn?: string;
    player_1_points?: string;
    player_2_points?: string;
    columns?: number;
    rows?: number;
    table_with_chips?: string;
  };
  date_time_from?: string;
  date_time_to?: string;
}

export interface Get_games {
  Games?:Game[];
}

export interface Game_post {
  Game?: Game;
}

export interface Game_full_info {
  id?: number;
  player_1?: User;
  player_2?: User;
  game_state?:{
    status?: string;
    turn?: string;
    player_1_points?: string;
    player_2_points?: string;
    columns?: number;
    rows?: number;
    table_with_chips?: string;
  };
  date_time_from?: string;
  date_time_to?: string;
}

export interface Get_game {
  Game?: Game_full_info;
}

export interface Game_state_update {
  Game_state_update?: {
    column_pos?: number;
    row_pos?: number;
    value?: string;
  }
}


