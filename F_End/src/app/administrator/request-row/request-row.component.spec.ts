import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RequestRowComponent } from './request-row.component';

describe('RequestRowComponent', () => {
  let component: RequestRowComponent;
  let fixture: ComponentFixture<RequestRowComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RequestRowComponent]
    });
    fixture = TestBed.createComponent(RequestRowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
