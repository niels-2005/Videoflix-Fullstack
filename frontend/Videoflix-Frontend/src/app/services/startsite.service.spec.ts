import { TestBed } from '@angular/core/testing';

import { StartsiteService } from './startsite.service';

describe('StartsiteService', () => {
  let service: StartsiteService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(StartsiteService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
