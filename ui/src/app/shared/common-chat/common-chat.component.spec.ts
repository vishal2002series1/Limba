import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommonChatComponent } from './common-chat.component';

describe('CommonChatComponent', () => {
  let component: CommonChatComponent;
  let fixture: ComponentFixture<CommonChatComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CommonChatComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CommonChatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
