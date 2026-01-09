```markdown
---
name: jasmine
description: |
  Jasmine/Karma unit testing for Angular components and services
  Use when: Writing or modifying unit tests for Angular components, services, or utilities in casino-f/ or casino-customer-f/
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Jasmine Skill

Jasmine/Karma testing framework for Angular 17 unit tests. This project uses Jasmine for assertions, Karma as the test runner, and Angular's testing utilities for component/service isolation. Tests live alongside source files as `*.spec.ts`.

## Quick Start

### Service Test with HTTP Mocking

```typescript
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { GameFilterService } from './game-filter.service';

describe('GameFilterService', () => {
  let service: GameFilterService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [GameFilterService]
    });
    service = TestBed.inject(GameFilterService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify(); // CRITICAL: Verify no outstanding requests
  });

  it('should fetch vendors', () => {
    const mockVendors = [{ id: 1, name: 'Vendor 1' }];
    
    service.getVendors().subscribe(vendors => {
      expect(vendors).toEqual(mockVendors);
    });

    const req = httpMock.expectOne('/api/v1/admin/vendors');
    expect(req.request.method).toBe('GET');
    req.flush(mockVendors);
  });
});
```

### Component Test with Spy Dependencies

```typescript
describe('PlayerListComponent', () => {
  let component: PlayerListComponent;
  let fixture: ComponentFixture<PlayerListComponent>;
  let playersServiceSpy: jasmine.SpyObj<PlayersService>;

  beforeEach(async () => {
    const spy = jasmine.createSpyObj('PlayersService', ['advancedPlayerSearch']);
    spy.advancedPlayerSearch.and.returnValue(of(mockPlayerList));

    await TestBed.configureTestingModule({
      imports: [PlayerListComponent, ReactiveFormsModule],
      providers: [{ provide: PlayersService, useValue: spy }],
      schemas: [NO_ERRORS_SCHEMA]
    }).compileComponents();

    playersServiceSpy = TestBed.inject(PlayersService) as jasmine.SpyObj<PlayersService>;
    fixture = TestBed.createComponent(PlayerListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should filter by KYC status', () => {
    component.filterForm.patchValue({ kycStatus: KycStatus.PARTIAL });
    component.loadPlayers();

    expect(playersServiceSpy.advancedPlayerSearch).toHaveBeenCalledWith(
      jasmine.objectContaining({ kycStatuses: [KycStatus.PARTIAL] }),
      jasmine.any(Number), jasmine.any(Number),
      jasmine.any(String), jasmine.any(String)
    );
  });
});
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `jasmine.createSpyObj` | Mock service with methods | `jasmine.createSpyObj('Svc', ['method'])` |
| `HttpTestingController` | Mock HTTP requests | `httpMock.expectOne(url)` |
| `NO_ERRORS_SCHEMA` | Ignore unknown elements | `schemas: [NO_ERRORS_SCHEMA]` |
| `fakeAsync/tick` | Control async timing | `fakeAsync(() => { tick(500); })` |
| `jasmine.objectContaining` | Partial object match | `jasmine.objectContaining({ key: value })` |

## Common Commands

```bash
cd casino-f && ng test              # Run admin frontend tests
cd casino-customer-f && ng test     # Run customer frontend tests
ng test --code-coverage             # Generate coverage report
ng test --include='**/service.spec.ts'  # Run specific tests
```

## See Also

- [patterns](references/patterns.md) - Testing patterns and anti-patterns
- [workflows](references/workflows.md) - Test setup and async workflows

## Related Skills

- See the **angular** skill for component architecture patterns
- See the **typescript** skill for type safety in tests
```