import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { ImageService } from '../services/image.service';
import { ImageData } from '../interfaces/image-data';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-request-details',
  templateUrl: './request-details.component.html',
  styleUrls: ['./request-details.component.css']
})
export class RequestDetailsComponent {

  @Input() id: number = 0;
  imageData: ImageData | null = null;
  isLoading: boolean = true;
  constructor(private router: Router, private imageService: ImageService) {}

  ngOnInit(): void {
    this.isLoading = true;
    this.imageService.getImage(this.id).subscribe({
      next: (imageData) => {
        this.imageData = imageData;
        this.isLoading = false;
      },
      error: (err) => {
        console.log(err);
        this.isLoading = false;
      }
    });
  }

  close(): void {
    this.router.navigate(['/user/browse-requests']);
  }

  signOut(): void{
    this.router.navigate(['/sign-in']);
  }
  appendToBaseUrl(fname: string | undefined): string{
    return `${environment.host}/api/serve-image/${fname}`;
  }
}
