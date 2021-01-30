export interface User {
  id?: number;
  user:{
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    password?: string;
  };
  phone: string;
  about: string;
  photo: string;
}

export interface Get_users {
  Users: User[];
}

export interface Get_user {
  User: User;
}

export interface Post_users_signup {
  User: User;
}

export interface Post_users_signin {
  User_signin: {
    username: string;
    password: string;
  };
}

export interface Patch_Users_userid {
  User_update: User;
}

export interface Photo_path {
  id: number,
  file: string
}


export interface User_main {
  Token: string;
  id: number;
}
