import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './header/header.component';
import { FormsModule } from '@angular/forms';
import { AngularMaterialModule } from '../angular-material/angular-material.module';
import { GridViewComponent } from './grid-view/grid-view.component';
import { RouterModule } from '@angular/router';
import { ImageDetailsComponent } from './image-details/image-details.component';
import { MatDialogModule } from '@angular/material/dialog';
import { ImageCardComponent } from './image-card/image-card.component';



@NgModule({
  declarations: [
    HeaderComponent,
    GridViewComponent,
    ImageDetailsComponent,
    ImageCardComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    AngularMaterialModule,
    RouterModule,
    MatDialogModule
  ],
  exports: [
    HeaderComponent,
    ImageDetailsComponent,
    MatDialogModule,
    ImageCardComponent
  ]
})
export class SharedModule { }
