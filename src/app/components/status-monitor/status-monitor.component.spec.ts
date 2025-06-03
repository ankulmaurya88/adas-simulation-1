import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StatusMonitorComponent } from './status-monitor.component';

describe('StatusMonitorComponent', () => {
  let component: StatusMonitorComponent;
  let fixture: ComponentFixture<StatusMonitorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StatusMonitorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StatusMonitorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
