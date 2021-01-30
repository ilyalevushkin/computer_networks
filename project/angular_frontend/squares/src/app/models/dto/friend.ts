import {User} from "./user";

export interface Friendship {
  user_friend?: User;
  friend?: User;
  status?: string;
}

export interface Get_friends {
  Friends?: Friendship[];
}

export interface Post_friends {
  Friendship?: {
    id?: number;
    status?: string;
  };
}

export interface Patch_friends_friendid {
  Status?: {
    ready_to_play?: boolean;
  };
}
