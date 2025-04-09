import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FinancialResponseComponent } from './financial-response.component';

describe('FinancialResponseComponent', () => {
  let component: FinancialResponseComponent;
  let fixture: ComponentFixture<FinancialResponseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FinancialResponseComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(FinancialResponseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
