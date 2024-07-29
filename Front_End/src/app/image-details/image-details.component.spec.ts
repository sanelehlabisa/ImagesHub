import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImageDetailsComponent } from './image-details.component';

describe('ImageDetailsComponent', () => {
  let component: ImageDetailsComponent;
  let fixture: ComponentFixture<ImageDetailsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ImageDetailsComponent]
    });
    fixture = TestBed.createComponent(ImageDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
