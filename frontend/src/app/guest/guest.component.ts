import { Component } from '@angular/core';

@Component({
  selector: 'app-guest',
  templateUrl: './guest.component.html',
  styleUrls: ['./guest.component.css']
})
export class GuestComponent {
  searchText: string;

  constructor() {
    this.searchText = "";
  }
}
