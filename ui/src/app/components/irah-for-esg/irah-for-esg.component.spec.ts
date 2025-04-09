import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IrahForEsgComponent } from './irah-for-esg.component';

describe('IrahForEsgComponent', () => {
  let component: IrahForEsgComponent;
  let fixture: ComponentFixture<IrahForEsgComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [IrahForEsgComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(IrahForEsgComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
