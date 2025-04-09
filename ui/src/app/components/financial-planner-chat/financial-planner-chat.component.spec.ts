import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FinancialPlannerChatComponent } from './financial-planner-chat.component';

describe('FinancialPlannerChatComponent', () => {
  let component: FinancialPlannerChatComponent;
  let fixture: ComponentFixture<FinancialPlannerChatComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FinancialPlannerChatComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FinancialPlannerChatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
