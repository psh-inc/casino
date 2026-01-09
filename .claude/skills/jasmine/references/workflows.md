```markdown
# Jasmine Testing Workflows

## Test Setup Workflow

### 1. Customer Frontend Test Polyfills

The customer frontend requires polyfills for certain global objects:

```typescript
// casino-customer-f/src/test-setup.ts
(window as any).global = window;
(window as any).process = {
  env: { DEBUG: undefined },
  version: '',
  nextTick: (fn: Function) => setTimeout(fn, 0)
};
(window as any).Buffer = (window as any).Buffer || {
  isBuffer: () => false
};

import '@angular/localize/init';
```

### 2. Standard Test Imports

```typescript
import { TestBed, ComponentFixture, fakeAsync, tick } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { of, throwError, BehaviorSubject } from 'rxjs';
```

---

## Async Testing Workflows

### fakeAsync with tick()

Use for operations with known delays:

```typescript
it('should trigger copyFromBonus after dialog closes', fakeAsync(() => {
  const dialogRefSpy = jasmine.createSpyObj('UiDialogRef', ['afterClosed']);
  dialogRefSpy.afterClosed.and.returnValue(of(mockBonus));
  dialogSpy.open.and.returnValue(dialogRefSpy);
  
  bonusServiceSpy.getAllBonusesForCopy.and.returnValue(of(mockBonuses));
  bonusServiceSpy.getBonusById.and.returnValue(of(mockBonus));

  component.openCopyDialog();
  tick();  // Process microtasks
  tick(500);  // Account for setTimeout delays

  expect(bonusServiceSpy.getBonusById).toHaveBeenCalledWith(mockBonus.id);
  expect(stateService.populateFormsFromBonus).toHaveBeenCalledWith(mockBonus);
}));
```

### done() Callback for Observable State Changes

Use when testing state transitions over time:

```typescript
it('should set exporting state during export', (done) => {
  const exportingStates: boolean[] = [];
  const subscription = service.isExportingDepositors$.subscribe(state => {
    exportingStates.push(state);
  });

  service.exportTopDepositors(mockFilters).subscribe({
    complete: () => {
      setTimeout(() => {
        expect(exportingStates).toContain(true);  // Was true during export
        expect(exportingStates[exportingStates.length - 1]).toBe(false);  // False after
        subscription.unsubscribe();
        done();
      }, 0);
    }
  });
});
```

---

## WARNING: Mixing fakeAsync with Real Async

**The Problem:**

```typescript
// BAD - HTTP calls don't work in fakeAsync without manual flushing
it('should fetch data', fakeAsync(() => {
  service.getData().subscribe(data => {
    expect(data).toBeTruthy();
  });
  tick();  // This doesn't flush HTTP requests!
}));
```

**Why This Breaks:**
1. `fakeAsync` virtualizes time but HTTP requests need `HttpTestingController`
2. `tick()` advances virtual timers, not actual network operations
3. Test may pass due to timing coincidence, then fail randomly

**The Fix:**

```typescript
// GOOD - Use HttpTestingController with fakeAsync
it('should fetch data', fakeAsync(() => {
  service.getData().subscribe(data => {
    expect(data).toBeTruthy();
  });

  const req = httpMock.expectOne('/api/data');
  req.flush({ result: 'success' });
  tick();  // Now tick() processes any follow-up timers
}));
```

---

## Error Testing Workflow

### HTTP Error Responses

```typescript
it('should handle validation errors', () => {
  const errorResponse = {
    status: 'ERROR',
    code: 'VALIDATION_FAILED',
    message: 'Validation failed',
    details: { fields: { email: 'Invalid email format' } }
  };

  service.createContent(invalidRequest).subscribe({
    next: () => fail('should have failed'),
    error: (error) => {
      expect(error.error).toEqual(errorResponse);
    }
  });

  const req = httpMock.expectOne(apiUrl);
  req.flush(errorResponse, { status: 400, statusText: 'Bad Request' });
});
```

### Observable Error Handling

```typescript
it('should handle export errors and reset state', (done) => {
  mockDashboardService.exportTopDepositors.and.returnValue(
    throwError(() => new Error('Export failed'))
  );

  const states: boolean[] = [];
  service.isExportingDepositors$.subscribe(state => states.push(state));

  service.exportTopDepositors(mockFilters).subscribe({
    error: () => {
      setTimeout(() => {
        expect(states).toContain(true);  // Started
        expect(states[states.length - 1]).toBe(false);  // Reset after error
        done();
      }, 0);
    }
  });
});
```

---

## Dialog Testing Workflow

```typescript
it('should open dialog and handle selection', fakeAsync(() => {
  const dialogRefSpy = jasmine.createSpyObj('UiDialogRef', ['afterClosed']);
  dialogRefSpy.afterClosed.and.returnValue(of(selectedItem));
  dialogSpy.open.and.returnValue(dialogRefSpy);

  component.openSelectionDialog();
  tick();

  expect(dialogSpy.open).toHaveBeenCalledWith(
    SelectionDialogComponent,
    jasmine.objectContaining({
      data: jasmine.objectContaining({ items: expectedItems })
    })
  );
  expect(component.selectedItem).toEqual(selectedItem);
}));
```

---

## DOM Testing Workflow

### Verify Template Rendering

```typescript
it('should show copy button in create mode', () => {
  component.isEditMode = false;
  fixture.detectChanges();

  const copySection = fixture.nativeElement.querySelector('.copy-from-bonus-section');
  expect(copySection).toBeTruthy();
});

it('should hide copy button in edit mode', () => {
  component.isEditMode = true;
  fixture.detectChanges();

  const copySection = fixture.nativeElement.querySelector('.copy-from-bonus-section');
  expect(copySection).toBeFalsy();
});

it('should show loading text', () => {
  component.loadingBonuses = true;
  fixture.detectChanges();

  const section = fixture.nativeElement.querySelector('.copy-from-bonus-section');
  expect(section?.textContent).toContain('Loading bonuses...');
});
```

---

## Test Organization

### Nested Describe Blocks

```typescript
describe('PlayerListComponent', () => {
  // Setup...

  describe('KYC Status Filter', () => {
    it('should filter by PARTIAL status', () => { /* ... */ });
    it('should filter by VERIFIED status', () => { /* ... */ });
    it('should clear KYC filter', () => { /* ... */ });
  });

  describe('Export Functionality', () => {
    it('should include filters in export request', () => { /* ... */ });
    it('should handle export errors', () => { /* ... */ });
  });
});
```

### Test Naming Convention

Start with "should" and describe the behavior:

```typescript
it('should filter players by PARTIAL KYC status', () => {});
it('should format registeredFrom date to LocalDateTime format', () => {});
it('should handle validation errors gracefully', () => {});
```

---

## Coverage Targets

- **Services**: 80% coverage
- **Components**: 70% coverage

```bash
ng test --code-coverage
# Report generated in coverage/
```

---

## Related Skills

- See the **angular** skill for component patterns being tested
- See the **playwright** skill for E2E testing workflows
```