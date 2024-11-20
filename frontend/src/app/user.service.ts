import { Injectable } from '@angular/core';
import { User } from './user';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})

export class UserService {
  private userSubject = new BehaviorSubject<User | null>(null);
  public user$ = this.userSubject.asObservable();

  public filterSubject = new BehaviorSubject<string>('');

  baseUrl: string = `${environment.host}/users`;

  

  constructor(private http: HttpClient) { }

  setFilter(filter: string): void {
    this.filterSubject.next(filter);
  }

  getFilter(): Observable<string> {
    return this.filterSubject.asObservable();
  }

  getUsers(): Observable<User[]> {
    
    return this.http.get<User[]>(this.baseUrl, {
      headers: this.getAuthHeader(),
      params: {}
    });
  }

  getUser(id: number): Observable<User[]> {
    
    return this.http.get<User[]>(`${this.baseUrl}/${id}`, {
      headers: this.getAuthHeader(),
      params: {}
    });
  }

  signIn(email: string): Observable<User> {
    let req = { email_address: email };
    return this.http.post<User>(
      `${environment.host}/auth`, req,
      {
        headers: this.getAuthHeader()
      }
    );
  }
  
  authorizeWithGoogle(): Observable<any> {
    let data = { step: 1 };
    return this.http.post<any>(
      `${environment.host}/users/google_auth`, data,
      {
        headers: this.getAuthHeader()
      }
    );
  }

  signInWithGoogle(): Observable<User> {

      let data = { step: 2 };
      return this.http.post<any>(
        `${environment.host}/users/google_auth`, data,
        {
          headers: this.getAuthHeader()
        }
      );
  }
  

  public getSignedInUser(): User | null {
    return this.userSubject.value;
  }

  public setUser(user: User | null): void {
    this.userSubject.next(user);
    localStorage.setItem('user', JSON.stringify(user)); // Store user in local storage
  }

  public isAuthenticated(userType: number): boolean {
    const user = this.getSignedInUser() || this.loadUserFromLocalStorage();
    if(user !== null) {
      if(userType == 0 && user?.type == 0) {
        return true;
      }

      if(userType == 1 && user?.type == 1) {
        return true;
      }
    }
    return false;
  }
  
  private loadUserFromLocalStorage(): User | null {
    const storedUser = localStorage.getItem('user');
    return storedUser ? JSON.parse(storedUser) : null;
  }

  private getAuthHeader(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${ environment.apiKey}`
    });
  }
}
