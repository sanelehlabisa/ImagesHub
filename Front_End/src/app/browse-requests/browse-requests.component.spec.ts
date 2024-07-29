import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BrowseRequestsComponent } from './browse-requests.component';

describe('BrowseRequestsComponent', () => {
  let component: BrowseRequestsComponent;
  let fixture: ComponentFixture<BrowseRequestsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [BrowseRequestsComponent]
    });
    fixture = TestBed.createComponent(BrowseRequestsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
