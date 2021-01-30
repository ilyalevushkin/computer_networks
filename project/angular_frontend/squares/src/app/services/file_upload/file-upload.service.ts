import { Injectable } from '@angular/core';
import {environment} from "../../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from 'rxjs';
import {Photo_path} from "../../models/dto/user";

@Injectable({
  providedIn: 'root'
})
export class FileUploadService {

  private url = `${environment.baseUrl}/api/v1/upload`;

  constructor(private http: HttpClient) { }

  public upload(formData: FormData) {
      return this.http.post<Photo_path>(`${this.url}`, formData);
  }
}
