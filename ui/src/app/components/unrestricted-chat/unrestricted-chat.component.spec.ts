import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnrestrictedChatComponent } from './unrestricted-chat.component';

describe('UnrestrictedChatComponent', () => {
  let component: UnrestrictedChatComponent;
  let fixture: ComponentFixture<UnrestrictedChatComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UnrestrictedChatComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UnrestrictedChatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
