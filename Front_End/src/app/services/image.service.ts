import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ImageData } from '../interfaces/image-data';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ImageService {

  baseUrl: string = `${environment.host}/api`;

  constructor(private http: HttpClient) { }

  private getAuthHeader(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'API_KEY': environment.API_KEY
    });
  }

  getImages(): Observable<ImageData[]> {
    return this.http.get<ImageData[]>(`${this.baseUrl}/get-images-data`, {
      headers: this.getAuthHeader()
    });
  }

  getImage(id: number): Observable<ImageData> {
    return this.http.get<ImageData>(`${this.baseUrl}/get-image-data/${id}`, {
      headers: this.getAuthHeader()
    });
  }
}
