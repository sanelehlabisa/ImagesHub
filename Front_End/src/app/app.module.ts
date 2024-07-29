import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SignInComponent } from './sign-in/sign-in.component';

import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowseImagesComponent } from './browse-images/browse-images.component';
import { BrowseRequestsComponent } from './browse-requests/browse-requests.component';
import { HeaderComponent } from './header/header.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AngularMaterialModule } from './angular-material/angular-material.module';
import { ScrollComponent } from './scroll/scroll.component';
import { ImageDetailsComponent } from './image-details/image-details.component';
import { RequestDetailsComponent } from './request-details/request-details.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
@NgModule({
  declarations: [
    AppComponent,
    SignInComponent,
    BrowseImagesComponent,
    BrowseRequestsComponent,
    HeaderComponent,
    ScrollComponent,
    ImageDetailsComponent,
    RequestDetailsComponent,
    PageNotFoundComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    AngularMaterialModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
