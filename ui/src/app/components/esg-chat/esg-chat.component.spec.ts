import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EsgChatComponent } from './esg-chat.component';

describe('EsgChatComponent', () => {
  let component: EsgChatComponent;
  let fixture: ComponentFixture<EsgChatComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EsgChatComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EsgChatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
