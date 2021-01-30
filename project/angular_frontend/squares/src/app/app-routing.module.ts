import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {ProfileComponent} from "./components/profile/profile.component";
import {AuthorizationComponent} from "./components/authorization/authorization.component";
import {RegistrationComponent} from "./components/registration/registration.component";
import {LogoutComponent} from "./components/logout/logout.component";
import {FriendListComponent} from "./components/friend-list/friend-list.component";
import {RouterModule, Routes} from "@angular/router";
import {GameComponent} from "./components/userspace/game/game.component";
import {RulesComponent} from "./components/userspace/rules/rules.component";
import {PullComponent} from "./components/userspace/pull/pull.component";
import {RegistrationSucceededComponent} from "./components/registration-succeeded/registration-succeeded.component";
import {AuthGuard} from "./components/_helpers/auth.guard";
import {FriendProfileComponent} from "./components/friend-profile/friend-profile.component";
import {GameSettingsComponent} from "./components/game-settings/game-settings.component";

const routes: Routes = [
    { path: 'game', component: GameComponent, canActivate: [AuthGuard] },
    { path: 'game_start', component: GameSettingsComponent, canActivate: [AuthGuard] },
    { path: 'rules', component: RulesComponent, canActivate: [AuthGuard] },
    { path: 'pull', component: PullComponent, canActivate: [AuthGuard] },
    { path: 'profile', component: ProfileComponent, canActivate: [AuthGuard] },
    { path: 'friend_profile', component: FriendProfileComponent, canActivate: [AuthGuard] },
    { path: 'login', component: AuthorizationComponent },
    { path: 'succeeded_signup', component: RegistrationSucceededComponent, canActivate: [AuthGuard] },
    { path: 'signup', component: RegistrationComponent },
    { path: 'logout', component: LogoutComponent },
    { path: 'friend_list', component: FriendListComponent, canActivate: [AuthGuard] },

    { path: '**', redirectTo: 'login' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
