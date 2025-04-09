import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrustReviewChatComponent } from './trust-review-chat.component';

describe('TrustReviewChatComponent', () => {
  let component: TrustReviewChatComponent;
  let fixture: ComponentFixture<TrustReviewChatComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TrustReviewChatComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TrustReviewChatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
