import { Component, Input, OnInit } from '@angular/core';
import { ImageDetailsComponent } from '../../shared/image-details/image-details.component';
import { MatDialog } from '@angular/material/dialog';
import { Image } from 'src/app/image';
import { environment } from 'src/environments/environment';
import { Link } from 'src/app/link';
import { LinkService } from 'src/app/link.service';

@Component({
  selector: 'app-image-card',
  templateUrl: './image-card.component.html',
  styleUrls: ['./image-card.component.css']
})
export class ImageCardComponent implements OnInit {
  
  @Input() image: Image | any = null;
  blobUrl: string = ""; // For displaying the image
  filename: string = "";

  constructor(private dialog: MatDialog, private linkService: LinkService) {

  }

  ngOnInit(): void {
    this.createBlobUrl(`${environment.host}/images/${this.image?.low_res_img_fname}`);
    this.filename = this.image.low_res_img_fname.substring(8);
  }

  async createBlobUrl(url: string) {
    try {
      const response = await fetch(url);
      const blob = await response.blob();
      this.blobUrl = URL.createObjectURL(blob);
    } catch (error) {
      console.error('Error fetching image:', error);
    }
  }

  generateLink(image_id: number): void {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const timestamp = Date.now().toString(); // Get the current timestamp
    let key = '';

    const limitLength = chars.length - 4;
    // Generate 4 random characters
    for (let i = chars.length - 1; limitLength < i; i--) {
      key += chars.indexOf(chars[i]);
      key += chars[Math.floor(Math.random() * chars.length)];
    }

    // Append the timestamp to the key
    key += timestamp;

    const link: Link = {
      id: 0,
      image_id: image_id,
      key: key,
      limit: 5
    }

    this.linkService.postLink(link).subscribe({
      next: res => { console.log(res) },
      error: err => { console.log(err) }
    })
  }

  async openImageModal(): Promise<void> {
    try {
      const response = await fetch(this.image.high_res_img_fname);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);

      this.dialog.open(ImageDetailsComponent, {
        width: 'auto',
        maxWidth: '100vw',  
        data: { imageUrl: url, filename: this.image.low_res_img_fname.substring(8) }
      });
    } catch (error) {
      console.error('Error fetching image:', error);
    }
  }
}
