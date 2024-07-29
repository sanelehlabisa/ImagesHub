import { Component, Input } from '@angular/core';
import { ImageData } from '../interfaces/image-data';
import { ImageService } from '../services/image.service';
import { Router } from '@angular/router';
import { UserService } from '../services/user.service';
import { RequestService } from '../services/request.service';
import { RequestData } from '../interfaces/request-data';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-image-details',
  templateUrl: './image-details.component.html',
  styleUrls: ['./image-details.component.css']
})
export class ImageDetailsComponent {
  @Input() id: number = 0;
  imageData: ImageData | any = null;
  guestRequests: RequestData[] = [];
  
  isRequestApproved: boolean = false;
  isLoading: boolean = true;

  constructor(
    private imageService: ImageService,
    private router: Router,
    private userService: UserService,
    private requestService: RequestService
  ) {}

  ngOnInit(): void {
    this.fetchImageData();
    this.fetchRequests();
  }

  fetchImageData(): void {
    this.isLoading = true;
    this.imageService.getImage(this.id).subscribe({
      next: imgData => {
        this.imageData = imgData;
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });
  }

  fetchRequests(): void {
    this.isLoading = true;
    this.requestService.getRequests().subscribe({
      next: requests => {
        const user = this.userService.getUser();
        if (user) {
          this.guestRequests = requests.filter(req => req.guest_id == user?.id && req.img_id == this.id);
          this.isRequestApproved = this.guestRequests.some(req => req.status === 1);
        } else {
          this.signOut();
        }
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });
  }

  close(): void {
    this.router.navigate(['/user/browse-images']);
  }

  sendRequest(reason: string): void {
    if (!reason) {
      alert("Oops, please enter the reason for requesting this image");
      return;
    }
    for (const request of this.guestRequests) {
      if (request.img_id == this.id) {
        alert("You have already submitted a request for this image, please wait for approval");
        return;
      }
    }

    const user = this.userService.getUser();
    if (!user) {
      alert("User not signed in");
      this.signOut();
      return;
    }

    let req: RequestData = {
      id: 0,
      img_id: this.id,
      guest_id: user.id,
      reason: reason,
      status: 0
    };
    
    this.isLoading = true;
    this.requestService.addRequest(req).subscribe({
      next: res => {
        alert("Request submitted successfully");
      },
      error: err => {
        console.log(err);
      }
    });
    this.fetchRequests();
    this.isLoading = false;
  }

  signOut(): void {
    this.router.navigate(['/sign-in']);
  }
  appendToBaseUrl(fname: string | undefined): string{
    return `${environment.host}/api/serve-image/${fname}`;
  }
}
