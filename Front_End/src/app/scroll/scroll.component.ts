import { Component } from '@angular/core';
import { ImageData } from '../interfaces/image-data';
import { angularMath } from 'angular-ts-math/dist/angular-ts-math/angular-ts-math';

@Component({
  selector: 'app-scroll',
  templateUrl: './scroll.component.html',
  styleUrls: ['./scroll.component.css']
})
export class ScrollComponent {
  page = 1;
  pageSize = 6 * 4;
  paginatedDataList: ImageData[] = [];
  dataList: ImageData[] = [];

  updatePaginatedItems() {
    const startIndex = (this.page - 1) * this.pageSize;
    const endIndex = startIndex + this.pageSize;
    this.paginatedDataList = this.dataList.slice(startIndex, endIndex);
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
    if (page >= 1 && page <= Math.ceil(this.dataList.length / this.pageSize)) {
      this.page = page;
      this.updatePaginatedItems();
    }
  }
  ceil(float: number): number{
    return angularMath.nextIntegerOfNumber(float) ;
  }
}
