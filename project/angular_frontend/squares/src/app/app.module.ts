import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './components/app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LogoutComponent } from './components/logout/logout.component';
import { FriendListComponent } from './components/friend-list/friend-list.component';
import { ProfileComponent } from './components/profile/profile.component';
import { RegistrationComponent } from './components/registration/registration.component';
import { AuthorizationComponent } from './components/authorization/authorization.component';
import { PanelComponent } from './components/userspace/common/panel/panel.component';
import { AppRoutingModule } from './app-routing.module';
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatGridListModule} from "@angular/material/grid-list";
import {MatIconModule} from "@angular/material/icon";
import {MatTabsModule} from "@angular/material/tabs";
import {MatButtonModule} from "@angular/material/button";
import {MatMenuModule} from "@angular/material/menu";
import { GameComponent } from './components/userspace/game/game.component';
import { PullComponent } from './components/userspace/pull/pull.component';
import { RulesComponent } from './components/userspace/rules/rules.component';
import { ScoreListComponent } from './components/userspace/game/score-list/score-list.component';
import { GameBlockComponent } from './components/userspace/game/game-block/game-block.component';
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatInputModule} from "@angular/material/input";
import { RegistrationSucceededComponent } from './components/registration-succeeded/registration-succeeded.component';
import {JwtInterceptor} from "./components/_helpers/jwt.interceptor";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { FriendProfileComponent } from './components/friend-profile/friend-profile.component';
import { GameSettingsComponent } from './components/game-settings/game-settings.component';
import {MatSelectModule} from "@angular/material/select";
import {MatOptionModule} from "@angular/material/core";

@NgModule({
  declarations: [
    AppComponent,
    LogoutComponent,
    FriendListComponent,
    ProfileComponent,
    RegistrationComponent,
    AuthorizationComponent,
    PanelComponent,
    GameComponent,
    PullComponent,
    RulesComponent,
    ScoreListComponent,
    GameBlockComponent,
    RegistrationSucceededComponent,
    FriendProfileComponent,
    GameSettingsComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    AppRoutingModule,
    MatToolbarModule,
    MatGridListModule,
    MatIconModule,
    MatTabsModule,
    MatButtonModule,
    MatMenuModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    ReactiveFormsModule,
    MatSelectModule,
    MatOptionModule
  ],
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass: JwtInterceptor,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
