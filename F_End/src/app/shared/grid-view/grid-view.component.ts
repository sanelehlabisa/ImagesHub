import { Component } from '@angular/core';
import { Image} from '../../image';
import { ImageService } from '../../image.service';
import { environment } from '../../../environments/environment';


@Component({
  selector: 'app-grid-view',
  templateUrl: './grid-view.component.html',
  styleUrls: ['./grid-view.component.css']
})
export class GridViewComponent {
 
  imagesList: Image[] = [];
  isLoading: boolean = true;

  constructor(private imageService: ImageService){}

  ngOnInit(): void{
    this.loadData();
  }
  
  onSearch(searchText: string): void {
    this.isLoading = true;
    if (searchText) {
      this.imagesList = this.imagesList.filter(image =>
        image.low_res_img_fname.toLowerCase().includes(searchText.toLowerCase())
      );
    } else {
      this.loadData();
    }
    this.isLoading = false;
  }

  loadData(): void{
    this.isLoading = true;
    this.imageService.getImages().subscribe({
      next: (imgsList) => {
        this.imagesList = imgsList;
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });
  }
}