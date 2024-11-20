import { Component } from '@angular/core';
import { Request } from '../../request';
import { RequestService } from '../../request.service';
import { UserService } from '../../user.service';
import { User } from '../../user';
import { ImageService } from '../../image.service';
import { Image } from 'src/app/image';

@Component({
  selector: 'app-table-view',
  templateUrl: './table-view.component.html',
  styleUrls: ['./table-view.component.css']
})
export class TableViewComponent {
  requestList: Request[] = [];
  imagesList: Image[] = [];
  userList: User[] = [];
  filteredRequestList: Request[] = [];

  isLoading: boolean = true;
  searchText: string = '';

  constructor(public imageService: ImageService, private requestService: RequestService, private userService: UserService) { }

  ngOnInit(): void {
    
    this.isLoading = true;

    this.requestService.getRequests().subscribe({
      next: requests => {
        this.requestList = requests;
        this.filteredRequestList = requests;
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });

    this.imageService.getImages().subscribe({
      next: images => {
        this.imagesList = images;
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });

    this.userService.getUsers().subscribe({
      next: users => {
        this.userList = users;
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });
    
    
    this.userService.filterSubject.subscribe(filter => {
      this.search(filter);
    });

  }

  search(emailAddress: string): void {
    this.filteredRequestList = [];

    if(emailAddress != "") {
      this.userList.forEach(user => {
        if(user.email_address.includes(emailAddress))
          this.requestList.forEach(request => {
            if(user.id == request.guest_id)
                this.filteredRequestList.push(request);
          });
      });
    } else {
      this.filteredRequestList = this.requestList;
    }
  }

  updateRequest(request: Request | any) : void {
    this.isLoading = true;
    this.requestService.updateRequest(request).subscribe({
      next: req => {
        this.updateRequestList(req);
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });
  }

  updateRequestList(request: Request) {
    this.isLoading = true;
    const index = this.requestList.findIndex(req => req.id === request.id);
    if (index !== -1) {
      this.requestList[index] = request;
    }
    this.isLoading = false;
  }
}
