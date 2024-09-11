import { EventEmitter, Injectable } from '@angular/core';
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

  baseUrl: string = `${environment.host}/users`;

  searchTextChanged = new EventEmitter<string>(); // Define the EventEmitter

  setSearchText(searchText: string): void {
    this.searchTextChanged.emit(searchText); // Emit the search text
  }

  constructor(private http: HttpClient) { }

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
      'Authorization': `Bearer ${ environment.API_KEY}`
    });
  }
}
