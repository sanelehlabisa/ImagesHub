import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SignInComponent } from './sign-in/sign-in.component';
import { BrowseImagesComponent } from './browse-images/browse-images.component';
import { BrowseRequestsComponent } from './browse-requests/browse-requests.component';
import { AppComponent } from './app.component';
import { ImageDetailsComponent } from './image-details/image-details.component';
import { RequestDetailsComponent } from './request-details/request-details.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { guestGuard } from './guards/guest.guard';
import { adminGuard } from './guards/admin.guard';

const routes: Routes = [
  { path: '', redirectTo: 'sign-in', pathMatch: 'full' },
  { path: 'sign-in', component: SignInComponent },
  {
    path: 'user', component: AppComponent, children: [
      { path: 'browse-images', component: BrowseImagesComponent, canActivate: [guestGuard] },
      { path: 'browse-images/details/:id', component: ImageDetailsComponent, canActivate: [guestGuard] },
      { path: 'browse-requests', component: BrowseRequestsComponent, canActivate: [adminGuard] },
      { path: 'browse-requests/details/:id', component: RequestDetailsComponent, canActivate: [adminGuard] }
    ]
  },
  { path: '404', component: PageNotFoundComponent },
  { path: '**', redirectTo: '404' }
];
@NgModule({
  imports: [RouterModule.forRoot(routes, {bindToComponentInputs:true})],
  exports: [RouterModule]
})
export class AppRoutingModule { }
