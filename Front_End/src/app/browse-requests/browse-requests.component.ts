import { Component } from '@angular/core';
import { RequestData } from '../interfaces/request-data';
import { RequestService } from '../services/request.service';
import { UserService } from '../services/user.service';
import { User } from '../interfaces/user';
import { angularMath } from 'angular-ts-math/dist/angular-ts-math/angular-ts-math';
import { ImageService } from '../services/image.service';

@Component({
  selector: 'app-browse-requests',
  templateUrl: './browse-requests.component.html',
  styleUrls: ['./browse-requests.component.css']
})
export class BrowseRequestsComponent {
  requestDataList: RequestData[] = [];
  userList: User[] = [];
  status: string[] = [
    "pending",
    "approved",
    "rejected"
  ];
  page = 1;
  pageSize = 15;
  paginatedRequestsData: RequestData[] = [];
  filteredData: RequestData[] = [];
  isLoading: boolean = true;

  constructor(public imageService: ImageService, private requestService: RequestService, private userService: UserService) { }

  ngOnInit(): void {
    this.isLoading = true;
    this.userService.getUsers().subscribe({
      next: users => {
        this.userList = users.filter(user => user.type == 0);
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });
    
    this.isLoading = true;
    this.requestService.getRequests().subscribe({
      next: requests => {
        this.requestDataList = requests;
        this.filteredData = requests
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });

  }

  addStatusStyleColor(status: number) {
    let color = 'orange';
    if (status == 1) {
      color = 'green';
    } else if (status == 2) {
      color = 'red';
    }
    return { color: (true) ? color : '' };
  }

  getEmail(id: number): string | any{
    return this.userList.find(user => user.id == id)?.email_address;
  }

  updateRequestData(resData: RequestData) {
    this.isLoading = true;
    const index = this.requestDataList.findIndex(item => item.id === resData.id);
    if (index !== -1) {
      this.requestDataList[index] = resData;
    }
    this.isLoading = false;
  }

  approveRequest(requestData: RequestData): void {
    this.isLoading = true;
    requestData.status = 1;
    this.requestService.updateRequest(requestData).subscribe({
      next: resData => {
        this.updateRequestData(resData);
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });
  }

  

  disapproveRequest(requestData: RequestData): void {
    this.isLoading = true;

    requestData.status = 2;
    this.requestService.updateRequest(requestData).subscribe({
      next: resData => {
        this.updateRequestData(resData);
      },
      error: err => {
        console.log(err);
      }
    });
    this.isLoading = false;
  }

  updatePaginatedItems() {
    const startIndex = (this.page - 1) * this.pageSize;
    const endIndex = startIndex + this.pageSize;
    this.paginatedRequestsData = this.filteredData.slice(startIndex, endIndex);
  }

  nextPage() {
    this.page++;
    this.updatePaginatedItems();
  }

  previousPage() {
    if (this.page > 1) {
      this.page--;
      this.updatePaginatedItems();
    }
  }

  setPage(page: number) {
    if (page >= 1 && page <= Math.ceil(this.filteredData.length / this.pageSize)) {
      this.page = page;
      this.updatePaginatedItems();
    }
  }
  ceil(float: number): number {
    return angularMath.nextIntegerOfNumber(float);
  }
  search(emailAddress: string) {
    this.isLoading = true;
    if (emailAddress) {
      let users: User[] = this.userList.filter(user => user.email_address.startsWith(emailAddress) && user.type == 0);

      this.filteredData = this.requestDataList.filter(reqData => {

        return users.filter(user => user.id == reqData.guest_id).length;
      });
    } else {
      this.filteredData = this.requestDataList;
    }
    this.isLoading = false;
  }
}
