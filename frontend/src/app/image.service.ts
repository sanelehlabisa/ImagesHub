import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Image } from './image';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ImageService {

  baseUrl: string = `${environment.host}/images`;

  constructor(private http: HttpClient) { }

  private getAuthHeader(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${ environment.apiKey}`
    });
  }

  getImages(): Observable<Image[]> {
    return this.http.get<Image[]>(this.baseUrl, {
      headers: this.getAuthHeader()
    });
  }

  getImage(id: number): Observable<Image> {
    return this.http.get<Image>(`${this.baseUrl}/${id}`, {
      headers: this.getAuthHeader()
    });
  }
}
