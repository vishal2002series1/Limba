import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HooppDemoChatComponent } from './hoopp-demo-chat.component';

describe('HooppDemoChatComponent', () => {
  let component: HooppDemoChatComponent;
  let fixture: ComponentFixture<HooppDemoChatComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HooppDemoChatComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(HooppDemoChatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
