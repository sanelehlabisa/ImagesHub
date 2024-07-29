import { Injectable } from '@angular/core';
import { User } from '../interfaces/user';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  baseUrl: string = `${environment.host}/api`;

  // Initialize the BehaviorSubject with a default value of null
  private userSubject = new BehaviorSubject<User | null>(null);
  // Expose the observable part of the subject
  user$ = this.userSubject.asObservable();

  constructor(private http: HttpClient) { }

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.baseUrl}/get-users-data`, {
      headers: this.getAuthHeader()
    });
  }

  signIn(email: string): Observable<User> {
    let req = { email_address: email };
    return this.http.post<User>(
      `${this.baseUrl}/sign-in`, req,
      {
        headers: this.getAuthHeader()
      }
    );
  }

  getUser(): User | null {
    return this.userSubject.value;
  }

  setUser(user: User): void {
    this.userSubject.next(user);
  }

  private getAuthHeader(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'API_KEY': environment.API_KEY
    });
  }
}
