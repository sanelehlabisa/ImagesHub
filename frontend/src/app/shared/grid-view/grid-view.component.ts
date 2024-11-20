import { Component } from '@angular/core';
import { Image} from '../../image';
import { ImageService } from '../../image.service';
import { UserService } from 'src/app/user.service';


@Component({
  selector: 'app-grid-view',
  templateUrl: './grid-view.component.html',
  styleUrls: ['./grid-view.component.css']
})
export class GridViewComponent {
 
  imagesList: Image[] = [];
  filteredImagesList: Image[] = [];

  isLoading: boolean = true;

  constructor(private imageService: ImageService, private userService: UserService){}

  ngOnInit(): void{
    this.loadData();
    this.userService.filterSubject.subscribe(filter => {
      this.search(filter);
    });

  }

  search(filename: string): void {
    this.filteredImagesList = [];
    if(filename != "") {
      this.imagesList.forEach(image => {
        if(image.low_res_img_fname.substring(8).toLowerCase().includes(filename.toLowerCase()))                
          this.filteredImagesList.push(image);
      });
    } else {
      this.filteredImagesList = this.imagesList;
    }
  }
  

  loadData(): void{
    this.isLoading = true;
    this.imageService.getImages().subscribe({
      next: (imgsList) => {
        this.imagesList = imgsList;
        this.filteredImagesList = imgsList;
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });
  }
}