import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserChatProdComponent } from './user-chat-prod.component';

describe('UserChatProdComponent', () => {
  let component: UserChatProdComponent;
  let fixture: ComponentFixture<UserChatProdComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UserChatProdComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserChatProdComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
