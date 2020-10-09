import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GroundingComponent } from './grounding.component';

describe('GroundingComponent', () => {
  let component: GroundingComponent;
  let fixture: ComponentFixture<GroundingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GroundingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GroundingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
