import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Link } from './link';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LinkService {

  baseUrl: string = `${environment.host}/links`;

  constructor(private http: HttpClient) { }

  private getAuthHeader(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${ environment.apiKey}`
    });
  }

  postLink(link: Link): Observable<Link> {
    return this.http.post<Link>(
      this.baseUrl, 
      link, 
      { headers: this.getAuthHeader() }
    );
  }
}
