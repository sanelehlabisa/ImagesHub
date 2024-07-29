import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {
  @Input() placeholder: string = "";
  @Output() searchEvent = new EventEmitter<string>();
  
  searchText: string = "";

  constructor(private router: Router){}

  search(): void{
    this.searchEvent.emit(this.searchText);
  }

  signOut(): void{
    this.router.navigate(['/sign-in']);
  }
}
