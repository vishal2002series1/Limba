import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RetirementServicePortalComponent } from './retirement-service-portal.component';

describe('RetirementServicePortalComponent', () => {
  let component: RetirementServicePortalComponent;
  let fixture: ComponentFixture<RetirementServicePortalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RetirementServicePortalComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RetirementServicePortalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
