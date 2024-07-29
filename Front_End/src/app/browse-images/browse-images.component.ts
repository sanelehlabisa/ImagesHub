import { Component } from '@angular/core';
import { ImageData } from '../interfaces/image-data';
import { ImageService } from '../services/image.service';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-browse-images',
  templateUrl: './browse-images.component.html',
  styleUrls: ['./browse-images.component.css']
})
export class BrowseImagesComponent {  
  imageDataList: ImageData[] = [];
  filteredImageDataList: ImageData[] = [];
  isLoading: boolean = true;

  constructor(private imageService: ImageService){}

  ngOnInit(): void{
    this.isLoading = true;
    this.imageService.getImages().subscribe({
      next: imgsDataList => {
        this.imageDataList = imgsDataList;
        this.filteredImageDataList = imgsDataList;
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });
  }
  onSearch(searchText: string): void {
    this.isLoading = true;
    if (searchText) {
      this.filteredImageDataList = this.imageDataList.filter(imageData =>
        imageData.low_res_img_fname.toLowerCase().includes(searchText.toLowerCase())
      );
    } else {
      this.filteredImageDataList = this.imageDataList;
    }
    this.isLoading = false;
  }
  appendToBaseUrl(fname: string | undefined): string{
    return `${environment.host}/api/serve-image/${fname}`;
  }
}
