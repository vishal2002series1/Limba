import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RetirementChatbotComponent } from './retirement-chatbot.component';

describe('RetirementChatbotComponent', () => {
  let component: RetirementChatbotComponent;
  let fixture: ComponentFixture<RetirementChatbotComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RetirementChatbotComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RetirementChatbotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
