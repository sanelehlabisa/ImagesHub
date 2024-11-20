import { Component, EventEmitter, Input, Output, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { UserService } from 'src/app/user.service';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  @Input() placeholder: string = "";
  @Input() isAdministrator: boolean = false;
  
  searchText: string = "";
  isRequestsActive: boolean = false;

  constructor(private router: Router, private userService: UserService) {}

  ngOnInit(): void {
    // Subscribe to router events to check for route changes
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe(() => {
      this.checkActiveRoute(); 
    });
    this.checkActiveRoute();
  }

  checkActiveRoute(): void {
    this.isRequestsActive = this.router.url.includes('requests'); // Update based on current URL
    this.placeholder = (this.isRequestsActive) ? "Search with requester Email Address..." : "Search with Image Filename...";
  }

  search(): void {
    this.userService.setFilter(this.searchText); 
  }

  signOut(): void {
    this.userService.setUser(null);
    this.router.navigate(['/sign-in']);
  }
}
