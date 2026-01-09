```markdown
# Jasmine Testing Patterns

## Service Testing Patterns

### HTTP Service Test Structure

```typescript
describe('ContentService', () => {
  let service: ContentService;
  let httpMock: HttpTestingController;
  const apiUrl = 'http://localhost:8080/api/v1/admin/content';

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ContentService]
    });
    service = TestBed.inject(ContentService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should verify request body', () => {
    const request = { contentTypeName: 'article', title: 'Test' };
    
    service.createContent(request).subscribe();

    const req = httpMock.expectOne(apiUrl);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(request);
    req.flush({ id: 1, ...request });
  });
});
```

### Query Parameter Verification

```typescript
it('should include pagination params', () => {
  service.getContents({ page: 0, size: 20, sort: 'createdAt,desc' }).subscribe();

  const req = httpMock.expectOne(r => r.url === apiUrl);
  expect(req.request.params.get('page')).toBe('0');
  expect(req.request.params.get('size')).toBe('20');
  expect(req.request.params.get('sort')).toBe('createdAt,desc');
  req.flush({ content: [], totalElements: 0 });
});
```

---

## Component Testing Patterns

### Standalone Component with Dependencies

```typescript
describe('BonusFormComponent', () => {
  let component: BonusFormComponent;
  let fixture: ComponentFixture<BonusFormComponent>;
  let bonusServiceSpy: jasmine.SpyObj<BonusService>;
  let dialogSpy: jasmine.SpyObj<UiDialogService>;

  beforeEach(async () => {
    const bonusSpy = jasmine.createSpyObj('BonusService', [
      'getAllBonusesForCopy', 'getBonusById', 'createBonus'
    ]);
    const dlgSpy = jasmine.createSpyObj('UiDialogService', ['open']);

    await TestBed.configureTestingModule({
      imports: [BonusFormComponent, ReactiveFormsModule, BrowserAnimationsModule],
      providers: [
        { provide: BonusService, useValue: bonusSpy },
        { provide: UiDialogService, useValue: dlgSpy }
      ],
      schemas: [NO_ERRORS_SCHEMA]
    }).compileComponents();

    bonusServiceSpy = TestBed.inject(BonusService) as jasmine.SpyObj<BonusService>;
    dialogSpy = TestBed.inject(UiDialogService) as jasmine.SpyObj<UiDialogService>;
    fixture = TestBed.createComponent(BonusFormComponent);
    component = fixture.componentInstance;
  });
});
```

### Form Testing

```typescript
it('should format date to LocalDateTime', () => {
  component.filterForm.patchValue({ registeredFrom: '2024-11-15' });
  component.loadPlayers();

  expect(playersServiceSpy.advancedPlayerSearch).toHaveBeenCalledWith(
    jasmine.objectContaining({ registeredFrom: '2024-11-15T00:00:00' }),
    jasmine.any(Number), jasmine.any(Number),
    jasmine.any(String), jasmine.any(String)
  );
});

it('should clear filters', () => {
  component.filterForm.patchValue({ kycStatus: KycStatus.PARTIAL });
  component.clearFilters();
  
  expect(component.filterForm.get('kycStatus')?.value).toBe('');
});
```

---

## WARNING: Forgetting afterEach Verify

**The Problem:**

```typescript
// BAD - No verification of outstanding requests
describe('MyService', () => {
  let httpMock: HttpTestingController;

  beforeEach(() => {
    // setup...
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('makes request', () => {
    service.getData().subscribe();
    // Missing httpMock.expectOne() or test ends without flushing
  });
  // No afterEach - outstanding requests go undetected
});
```

**Why This Breaks:**
1. Unverified requests mask bugs where extra calls are made
2. Tests pass but production code makes duplicate API calls
3. Memory leaks from hanging subscriptions in real app

**The Fix:**

```typescript
// GOOD - Always verify no outstanding requests
afterEach(() => {
  httpMock.verify();
});
```

---

## WARNING: Testing Synchronous Code with done()

**The Problem:**

```typescript
// BAD - Using done() for synchronous observable
it('should get data', (done) => {
  service.getCachedData().subscribe(data => {
    expect(data).toBeTruthy();
    done();
  });
});
```

**Why This Breaks:**
1. If observable completes synchronously, test passes but `done()` is unnecessary overhead
2. If subscription throws, `done()` is never called and test times out with unhelpful message
3. Timeout failures mask the real error

**The Fix:**

```typescript
// GOOD - Synchronous observables don't need done()
it('should get cached data', () => {
  service.getCachedData().subscribe(data => {
    expect(data).toBeTruthy();
  });
});

// Use done() ONLY for truly async operations like setTimeout
it('should emit after delay', (done) => {
  service.delayedEmit().subscribe({
    next: data => expect(data).toBeTruthy(),
    complete: () => done()
  });
});
```

---

## WARNING: Missing NO_ERRORS_SCHEMA

**The Problem:**

```typescript
// BAD - Must import every child component
await TestBed.configureTestingModule({
  imports: [
    ParentComponent,
    ChildComponent1, ChildComponent2, ChildComponent3,
    SharedComponent1, SharedComponent2, // ... many more
  ]
}).compileComponents();
```

**Why This Breaks:**
1. Test setup becomes brittle - adding components requires updating tests
2. Tests are slow due to compiling unnecessary components
3. Component isolation is lost - child component bugs affect parent tests

**The Fix:**

```typescript
// GOOD - Use NO_ERRORS_SCHEMA for component isolation
import { NO_ERRORS_SCHEMA } from '@angular/core';

await TestBed.configureTestingModule({
  imports: [ParentComponent, ReactiveFormsModule],
  providers: [{ provide: MyService, useValue: mockService }],
  schemas: [NO_ERRORS_SCHEMA]
}).compileComponents();
```

**When You Might Be Tempted:**
When testing components with many custom UI elements (`<ui-button>`, `<ui-modal>`, etc.) and you get template errors.

---

## Spy Method Patterns

### Return Different Values Per Call

```typescript
const spy = jasmine.createSpyObj('Svc', ['getData']);
spy.getData.and.returnValues(
  of({ first: true }),
  of({ second: true })
);

// First call returns { first: true }
// Second call returns { second: true }
```

### Verify Call Arguments

```typescript
expect(spy.advancedSearch).toHaveBeenCalledWith(
  jasmine.objectContaining({ status: 'ACTIVE' }),
  jasmine.any(Number),
  jasmine.stringContaining('desc')
);

// Get specific call arguments
const firstCallArgs = spy.advancedSearch.calls.first().args;
const lastCallArgs = spy.advancedSearch.calls.mostRecent().args;
```

---

## Related Skills

- See the **angular** skill for component lifecycle and dependency injection
- See the **typescript** skill for interface definitions in tests
```