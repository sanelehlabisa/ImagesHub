import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { GuestRoutingModule } from './guest-routing.module';
import { GuestComponent } from './guest.component';

import { SharedModule } from '../shared/shared.module';
import { AngularMaterialModule } from '../angular-material/angular-material.module';
import { RequestDetailsComponent } from './request-details/request-details.component';


@NgModule({
  declarations: [
    GuestComponent,
    RequestDetailsComponent
  ],
  imports: [
    CommonModule,
    GuestRoutingModule,
    AngularMaterialModule,
    SharedModule
  ]
})
export class GuestModule {
  constructor(){
    console.log('Guest Module loaded');
  }
 }