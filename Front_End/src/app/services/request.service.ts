import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { RequestData } from '../interfaces/request-data';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RequestService {

  baseUrl: string = `${environment.host}/api`;

  constructor(private http: HttpClient) { }

  private getAuthHeader(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'API_KEY': environment.API_KEY
    });
  }

  getRequest(id: number): Observable<RequestData> {
    return this.http.get<RequestData>(`${this.baseUrl}/get-request-data/${id}`, {
      headers: this.getAuthHeader()
    });
  }

  getRequests(): Observable<RequestData[]> {
    return this.http.get<RequestData[]>(`${this.baseUrl}/get-requests-data`, {
      headers: this.getAuthHeader()
    });
  }

  updateRequest(requestData: RequestData): Observable<RequestData> {
    return this.http.put<RequestData>(
      `${this.baseUrl}/update-request-data`, 
      requestData, 
      { headers: this.getAuthHeader() }
    );
  }

  addRequest(requestData: RequestData): Observable<RequestData> {
    return this.http.post<RequestData>(
      `${this.baseUrl}/post-request-data`, 
      requestData, 
      { headers: this.getAuthHeader() }
    );
  }
}
