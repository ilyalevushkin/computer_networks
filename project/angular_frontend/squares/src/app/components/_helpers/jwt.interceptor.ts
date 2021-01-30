import { Injectable } from '@angular/core';
import {HttpRequest, HttpHandler, HttpEvent, HttpInterceptor} from '@angular/common/http';
import { Observable } from 'rxjs';
import {AuthenticationService} from "../../services/auth/authentication.service";


@Injectable()
export class JwtInterceptor implements HttpInterceptor {

    constructor(private authenticationService: AuthenticationService) { }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        let currentUser = this.authenticationService.currentUserValue;
        if (currentUser && currentUser.Token) {
          request = request.clone({
            setHeaders: {
              Authorization: `Token ${currentUser.Token}`
            }
          });
        }
        if (request.url !== "http://localhost:8000/api/v1/upload")
        {
          request = request.clone({
          setHeaders: {'Content-Type': 'application/json'}
          });
        }
        return next.handle(request);
    }
}
