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

  isLoading: boolean = true;
  searchText: string = '';

  constructor(public imageService: ImageService, private requestService: RequestService, private userService: UserService) { }

  ngOnInit(): void {
    this.userService.searchTextChanged.subscribe(searchText => {
      this.search(searchText);
    });

    
    this.isLoading = true;

    this.requestService.getRequests().subscribe({
      next: requests => {
        this.requestList = requests;
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });

    this.imageService.getImages().subscribe({
      next: image => {
        this.imagesList = image;
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });
  }

  search(emailAddress: string): void {
    console.log("Here")
    this.requestList.filter((request) => {
      const user = this.userList.find(user => emailAddress === user?.email_address);
      return request?.guest_id === user?.id;
    });
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
