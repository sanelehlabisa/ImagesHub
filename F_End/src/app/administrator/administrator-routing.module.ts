import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { administratorGuard } from './administrator.guard';
import { GridViewComponent } from '../shared/grid-view/grid-view.component';
import { TableViewComponent } from './table-view/table-view.component';
import { AdministratorComponent } from './administrator.component';

const routes: Routes = [
  { path: '', component: AdministratorComponent,
    children: [
      { path: '', redirectTo: 'browse-requests', pathMatch: 'full' },
      { path: 'browse-requests', component: TableViewComponent, canActivate: [administratorGuard] },
      { path: 'browse-images', component: GridViewComponent, canActivate: [administratorGuard] }
    ]
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdministratorRoutingModule { }
