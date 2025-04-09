import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FinancialChatComponent } from './financial-chat.component';

describe('FinancialChatComponent', () => {
  let component: FinancialChatComponent;
  let fixture: ComponentFixture<FinancialChatComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FinancialChatComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FinancialChatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
