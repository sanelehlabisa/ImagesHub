import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BrowseImagesComponent } from './browse-images.component';

describe('BrowseImagesComponent', () => {
  let component: BrowseImagesComponent;
  let fixture: ComponentFixture<BrowseImagesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [BrowseImagesComponent]
    });
    fixture = TestBed.createComponent(BrowseImagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
