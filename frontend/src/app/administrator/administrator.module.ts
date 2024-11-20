import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AdministratorRoutingModule } from './administrator-routing.module';
import { AdministratorComponent } from './administrator.component';
import { TableViewComponent } from './table-view/table-view.component';
import { RequestRowComponent } from './request-row/request-row.component';
import { AngularMaterialModule } from '../angular-material/angular-material.module';
import { SharedModule } from '../shared/shared.module';



@NgModule({
  declarations: [
    AdministratorComponent,
    TableViewComponent,
    RequestRowComponent
  ],
  imports: [
    CommonModule,
    AdministratorRoutingModule,
    AngularMaterialModule,
    SharedModule
  ],
  bootstrap: [AdministratorComponent]
})
export class AdministratorModule { 
  constructor(){
    console.log('Adimnistrator Module loaded');
  }
}
