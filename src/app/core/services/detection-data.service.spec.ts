import { TestBed } from '@angular/core/testing';

import { DetectionDataService } from './detection-data.service';

describe('DetectionDataService', () => {
  let service: DetectionDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DetectionDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
