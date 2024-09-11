import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Email } from './email';

@Injectable({
  providedIn: 'root'
})
export class EmailService {
  baseUrl: string;
  
  constructor(private http: HttpClient) { 
    this.baseUrl = `${environment.host}/emails`;
  }

  private getAuthHeader(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${ environment.API_KEY}`
    });
  }

  postEmail(email: Email): Observable<Email> {
    return this.http.post<Email>(
      this.baseUrl,
      email,
      { headers: this.getAuthHeader() }
    );
  }
}
