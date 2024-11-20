import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ImageDetailsComponent } from '../../shared/image-details/image-details.component';
import { User } from 'src/app/user';
import { Image } from 'src/app/image';
import { environment } from 'src/environments/environment';
import { UserService } from 'src/app/user.service';
import { ImageService } from 'src/app/image.service';
import { EmailService } from 'src/app/email.service';
import { Email } from 'src/app/email';

@Component({
  selector: 'app-request-row',
  templateUrl: './request-row.component.html',
  styleUrls: ['./request-row.component.css']
})
export class RequestRowComponent {
  user: User | any = null;
  image: Image | any = null;

  @Input() request: Request | any = null;
  @Input() index: number = 0;

  @Output() updateEvent = new EventEmitter<Request>();

  status: string[] = [
    "Pending",
    "Approved",
    "Rejected"
  ];

  constructor(private dialog: MatDialog, private userService: UserService, private imageService: ImageService, private emailService: EmailService) {}

  ngOnInit() :void {
    this.userService.getUser(this.request.guest_id).subscribe({
      next: user => this.user = user,
      error: err => console.log(err) 
    });

    this.imageService.getImage(this.request.image_id).subscribe({
      next: image => this.image = image,
      error: err => console.log(err) 
    });
  }

  addStatusStyleColor(status: number): any {
    let color = 'orange';
    if (status == 1) {
      color = 'green';
    } else if (status == 2) {
      color = 'red';
    }
    return { color: (true) ? color : '' };
  }

  getEmailAddress(): string | any{
    return this.user?.email_address;
  }

  getImageUrl(): string{
    return `${environment.host}/images/${this.image?.high_res_img_fname}`;
  }

  getImageFilename(): string | any {
    if (this.image) {
        const lowResImgFname = this.image?.low_res_img_fname;

        // Remove unwanted characters and the file extension
        const cleanedName = lowResImgFname
            .replace(/[-_.]/g, ' ') // Replace - , _ , . with space
            .split('.')[0]          // Remove file extension
            .trim();                // Trim whitespace

        // Limit to max length of 8 characters
        let result = cleanedName.length > 15 ? cleanedName.substring(7, 15) + '...' : cleanedName;

        return result;
    }
    return null;
  }
  
  updateRequest(status: number): void {
    if(this.request) {
      this.request.status = status;
      if(status == 1) {
        const email: Email = {
          receiver_email_address: this.getEmailAddress(),
          subject: "Images Hub Request Approved",
          body: `Hi\n\nWe hope this email finds you well.\n\nWe would like to let you know that your request to access image ${this.image.low_res_img_fname} has been approved.\n\nThanks\n\nKind Regards\nImages Hub Team`
        }
        this.emailService.postEmail(email).subscribe({
          next: ()=> {},
          error: (err)=> console.log(err)
        })

      }

      this.updateEvent.emit(this.request);
    }
  }

  openImageModal(imageUrl: string): void {
    this.dialog.open(ImageDetailsComponent, {
      data: { imageUrl: imageUrl, filename: this.image.low_res_img_fname.substring(8) }
    });
  }
}
