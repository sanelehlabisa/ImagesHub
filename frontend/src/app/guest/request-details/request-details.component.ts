import { Component, Inject } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Image } from 'src/app/image';
import { Request } from 'src/app/request';
import { RequestService } from 'src/app/request.service';
import { UserService } from 'src/app/user.service';

@Component({
  selector: 'app-request-details',
  templateUrl: './request-details.component.html',
  styleUrls: ['./request-details.component.css']
})
export class RequestDetailsComponent {
  private request: Request | any = null;
  private regExp: string = '^[a-zA-Z0-9_]*$';
  public formGroup = new FormGroup({
    reason: new FormControl('',[
      Validators.required,
      Validators.pattern(this.regExp)
    ]
    )
  });

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { image: Image },
    private dialogRef: MatDialogRef<RequestDetailsComponent>, private requestService: RequestService, private userService: UserService
  ) {}

  ngOnInit(): void {
    this.requestService.getRequests().subscribe({
      next: (reqs) => {
        const req = reqs.filter(req => req.guest_id == this.userService.getSignedInUser()?.id || req.image_id == this.data.image.id);
        if(req){
          this.request = req[0];
        }
      },
      error: (err) => console.log(err)
    });
  }
 
  get reason() {
    return this.formGroup.get('reason')
  }

  submitRequest(): void {
    if(this.request) {
      alert(`You have already submitted a request for this image, please wait for approval`);
    } else {
      const req: Request = {
        id: 0,
        guest_id: this.userService.getSignedInUser()?.id || 0,
        image_id: this.data.image.id,
        reason: this.reason?.value || '',
        status: 0
      }
      this.requestService.addRequest(req).subscribe({
        next: res => { alert(`You have succesfully submitted a request for an image ${this.data.image.high_res_img_fname.substring(8)}, please wait for approval`); },
        error: err => { console.log(err) }
      })
    }
  }

  close(): void {
    this.dialogRef.close(); // Close the dialog
  }
}
