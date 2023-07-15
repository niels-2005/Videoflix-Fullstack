import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImprintPpComponent } from './imprint-pp.component';

describe('ImprintPpComponent', () => {
  let component: ImprintPpComponent;
  let fixture: ComponentFixture<ImprintPpComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ImprintPpComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ImprintPpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
