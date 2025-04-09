import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WealthChatComponent } from './wealth-chat.component';

describe('WealthChatComponent', () => {
  let component: WealthChatComponent;
  let fixture: ComponentFixture<WealthChatComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WealthChatComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WealthChatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
