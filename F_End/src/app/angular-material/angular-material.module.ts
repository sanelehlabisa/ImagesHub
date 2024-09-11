import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

const matertialComponent = [
  MatIconModule,
  MatProgressSpinnerModule
];

@NgModule({
  declarations: [],
  imports: [
    CommonModule
  ],
  exports: [
    matertialComponent
  ]
})
export class AngularMaterialModule { }
