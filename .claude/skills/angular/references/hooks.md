# Angular Lifecycle Hooks & Cleanup Patterns

## Overview

Every component and service with subscriptions MUST implement proper cleanup. This codebase uses the `destroy$` pattern consistently across all components.

## The Destroy Pattern

### Component Implementation

```typescript
@Component({
  selector: 'app-header-new',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HeaderNewComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  ngOnInit(): void {
    this.authService.currentUser$
      .pipe(takeUntil(this.destroy$))
      .subscribe(user => this.handleUserChange(user));

    this.walletService.getWalletSummary()
      .pipe(takeUntil(this.destroy$))
      .subscribe(summary => this.updateBalance(summary));

    this.router.events
      .pipe(
        filter(event => event instanceof NavigationEnd),
        takeUntil(this.destroy$)
      )
      .subscribe(() => this.setCurrentPageFromRoute());
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

### Service Implementation

```typescript
@Injectable({ providedIn: 'root' })
export class WalletV2Service implements OnDestroy {
  private destroy$ = new Subject<void>();
  private balanceRefreshTimer$ = timer(0, 30000);

  startBalanceRefresh(playerId: number): void {
    this.balanceRefreshTimer$.pipe(
      takeUntil(this.destroy$),
      switchMap(() => this.fetchPlayerBalance(playerId)),
      catchError(error => {
        console.error('Balance refresh error:', error);
        return of(null);
      })
    ).subscribe(balance => {
      if (balance) this.playerBalance$.next(balance);
    });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

---

## WARNING: Subscribing Without Cleanup

**The Problem:**

```typescript
// BAD - Memory leak, zombie subscription
ngOnInit(): void {
  this.service.someData().subscribe(data => {
    this.data = data;
  });
}
```

**Why This Breaks:**
1. Subscription persists after component destruction
2. Memory leak accumulates with each navigation
3. Callbacks execute on destroyed components, causing errors
4. Multiple subscriptions pile up if user navigates back

**The Fix:**

```typescript
// GOOD - Properly cleaned up
private destroy$ = new Subject<void>();

ngOnInit(): void {
  this.service.someData().pipe(
    takeUntil(this.destroy$)
  ).subscribe(data => {
    this.data = data;
  });
}

ngOnDestroy(): void {
  this.destroy$.next();
  this.destroy$.complete();
}
```

**When You Might Be Tempted:**
Quick prototyping, simple one-time HTTP calls (even these should use `take(1)` or async pipe).

---

## WARNING: Forgetting to Complete destroy$

**The Problem:**

```typescript
// BAD - Subject never completed
ngOnDestroy(): void {
  this.destroy$.next();
  // Missing: this.destroy$.complete();
}
```

**Why This Breaks:**
1. Subject remains in memory
2. Any operators depending on completion won't finalize
3. Potential for subtle memory leaks in long-running apps

**The Fix:**

```typescript
// GOOD - Both next() and complete()
ngOnDestroy(): void {
  this.destroy$.next();
  this.destroy$.complete();
}
```

---

## OnInit vs Constructor

### Constructor: Dependency Injection Only

```typescript
// GOOD - Only DI in constructor
constructor(
  private playerService: PlayerService,
  private router: Router,
  private fb: FormBuilder
) {}
```

### OnInit: Initialization Logic

```typescript
// GOOD - All setup in ngOnInit
ngOnInit(): void {
  this.initializeForm();
  this.loadInitialData();
  this.subscribeToRouteChanges();
}
```

---

## AfterViewInit for DOM Operations

```typescript
@Component({...})
export class GamesListComponent implements OnInit, AfterViewInit {
  @ViewChild('scrollContainer') scrollContainer!: ElementRef;

  ngAfterViewInit(): void {
    // DOM is now available
    if (this.isCarousel) {
      setTimeout(() => this.checkScrollButtons(), 200);
    }
  }
}
```

---

## Angular 17+ takeUntilDestroyed

For newer Angular 17 code, prefer `takeUntilDestroyed()`:

```typescript
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

@Component({...})
export class ModernComponent {
  private destroyRef = inject(DestroyRef);

  ngOnInit(): void {
    this.service.data$.pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe(data => this.handleData(data));
  }
}
```

---

## Quick Reference

| Hook | Use For | Example |
|------|---------|---------|
| `constructor` | Dependency injection only | `private service: Service` |
| `ngOnInit` | Subscriptions, initial data load | `this.loadData()` |
| `ngAfterViewInit` | DOM manipulation, ViewChild access | `this.element.nativeElement` |
| `ngOnDestroy` | Cleanup subscriptions | `this.destroy$.next()` |
| `ngOnChanges` | React to @Input changes | `if (changes['playerId'])` |