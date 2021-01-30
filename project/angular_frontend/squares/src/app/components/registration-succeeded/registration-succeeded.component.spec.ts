import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegistrationSucceededComponent } from './registration-succeeded.component';

describe('RegistrationSucceededComponent', () => {
  let component: RegistrationSucceededComponent;
  let fixture: ComponentFixture<RegistrationSucceededComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RegistrationSucceededComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RegistrationSucceededComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
