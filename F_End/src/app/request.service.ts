import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Request } from './request';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RequestService {

  baseUrl: string = `${environment.host}/requests`;

  constructor(private http: HttpClient) { }

  private getAuthHeader(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${ environment.API_KEY}`
    });
  }

  getRequest(id: number): Observable<Request> {
    return this.http.get<Request>(`${this.baseUrl}/${id}`, {
      headers: this.getAuthHeader()
    });
  }

  getRequests(): Observable<Request[]> {
    return this.http.get<Request[]>(this.baseUrl, {
      headers: this.getAuthHeader()
    });
  }

  updateRequest(requestData: Request): Observable<Request> {
    return this.http.put<Request>(
      this.baseUrl, 
      requestData, 
      { headers: this.getAuthHeader() }
    );
  }

  addRequest(requestData: Request): Observable<Request> {
    return this.http.post<Request>(
      this.baseUrl, 
      requestData, 
      { headers: this.getAuthHeader() }
    );
  }
}
