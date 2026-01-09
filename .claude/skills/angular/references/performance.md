# Angular Performance Patterns

## OnPush Change Detection

**ALWAYS use OnPush** for components that don't require default change detection.

### Basic OnPush Pattern

```typescript
@Component({
  selector: 'app-game-card',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class GameCardComponent {
  @Input() game!: GameDto;  // Only re-checks when input reference changes
}
```

### When OnPush Re-renders

1. Input reference changes (not mutation!)
2. Event originates from component or child
3. Async pipe receives new value
4. Manual `markForCheck()` called

---

## WARNING: Missing trackBy in ngFor

**The Problem:**

```html
<!-- BAD - No trackBy -->
<div *ngFor="let game of games">
  <app-game-card [game]="game"></app-game-card>
</div>
```

**Why This Breaks:**
1. Entire list re-rendered on any change
2. DOM elements destroyed and recreated
3. Lost scroll position, animations break
4. Poor performance with large lists

**The Fix:**

```typescript
trackByGameId(index: number, game: GameDto): string {
  return game.id;
}
```

```html
<!-- GOOD - With trackBy -->
<div *ngFor="let game of games; trackBy: trackByGameId">
  <app-game-card [game]="game"></app-game-card>
</div>
```

---

## WARNING: Calling Functions in Templates

**The Problem:**

```html
<!-- BAD - Called on every change detection cycle -->
<div>{{ calculateTotal() }}</div>
<div *ngIf="isEligible()">Eligible</div>
```

**Why This Breaks:**
1. Function runs on EVERY change detection
2. No caching of results
3. Exponential performance degradation

**The Fix:**

```typescript
// GOOD - Use getter or computed property
get total(): number {
  return this.items.reduce((sum, item) => sum + item.price, 0);
}

get isEligible(): boolean {
  return this.user?.kycStatus === 'VERIFIED' && this.balance > 0;
}
```

```html
<div>{{ total }}</div>
<div *ngIf="isEligible">Eligible</div>
```

**For complex calculations:**

```typescript
// Store in property, update only when needed
ngOnInit(): void {
  this.calculateTotals();
}

private calculateTotals(): void {
  this.totalAmount = this.items.reduce((sum, item) => sum + item.price, 0);
  this.itemCount = this.items.length;
}
```

---

## WARNING: Manual Change Detection

**The Problem:**

```typescript
// BAD - Fighting the framework
constructor(private cdr: ChangeDetectorRef) {}

updateData(): void {
  this.data = newData;
  this.cdr.detectChanges();  // Red flag!
}
```

**Why This Breaks:**
1. Usually indicates architectural problem
2. Can cause performance issues
3. Makes debugging difficult
4. Breaks OnPush strategy

**The Fix:**

```typescript
// GOOD - Use immutable updates with OnPush
updateData(): void {
  this.data = { ...this.data, ...newData };  // New reference triggers detection
}

// Or use BehaviorSubject with async pipe
data$ = new BehaviorSubject<Data>(initialData);

updateData(): void {
  this.data$.next(newData);  // Async pipe handles detection
}
```

---

## Lazy Loading

### Route-Based Lazy Loading

```typescript
// app.routes.ts
export const routes: Routes = [
  {
    path: 'games',
    loadComponent: () => import('./features/games/games.component')
      .then(m => m.GamesComponent)
  },
  {
    path: 'wallet',
    loadChildren: () => import('./features/wallet/wallet.routes')
      .then(m => m.WALLET_ROUTES)
  }
];
```

### Component Lazy Loading

```typescript
@Component({
  selector: 'app-dashboard',
  template: `
    <ng-container *ngIf="showChart">
      <ng-container *ngComponentOutlet="chartComponent"></ng-container>
    </ng-container>
  `
})
export class DashboardComponent {
  chartComponent: Type<any> | null = null;

  async loadChart(): Promise<void> {
    const { ChartComponent } = await import('./chart/chart.component');
    this.chartComponent = ChartComponent;
  }
}
```

---

## Virtualization for Large Lists

For lists with 100+ items, use virtual scrolling:

```typescript
import { ScrollingModule } from '@angular/cdk/scrolling';

@Component({
  standalone: true,
  imports: [ScrollingModule],
  template: `
    <cdk-virtual-scroll-viewport itemSize="50" class="viewport">
      <div *cdkVirtualFor="let item of items; trackBy: trackById">
        {{ item.name }}
      </div>
    </cdk-virtual-scroll-viewport>
  `
})
export class LargeListComponent {
  items: Item[] = [];  // Can have thousands
  
  trackById(index: number, item: Item): number {
    return item.id;
  }
}
```

---

## Pure Pipes for Transformations

```typescript
@Pipe({
  name: 'formatCurrency',
  standalone: true,
  pure: true  // Default, only recalculates when input changes
})
export class FormatCurrencyPipe implements PipeTransform {
  transform(value: number, currency = 'EUR'): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency
    }).format(value);
  }
}
```

```html
<!-- Cached result, only recalculates when value or currency changes -->
<span>{{ balance | formatCurrency:'USD' }}</span>
```

---

## Debouncing User Input

```typescript
@Component({...})
export class SearchComponent implements OnInit, OnDestroy {
  searchControl = new FormControl('');
  private destroy$ = new Subject<void>();

  ngOnInit(): void {
    this.searchControl.valueChanges.pipe(
      debounceTime(300),  // Wait 300ms after last keystroke
      distinctUntilChanged(),  // Ignore if same value
      switchMap(term => this.searchService.search(term)),
      takeUntil(this.destroy$)
    ).subscribe(results => this.results = results);
  }
}
```

---

## Bundle Size Optimization

### Import Specific Modules

```typescript
// BAD - Imports entire library
import * as _ from 'lodash';

// GOOD - Import only what you need
import { debounce } from 'lodash-es';
```

### Tree-Shakeable Services

```typescript
// GOOD - Tree-shakeable
@Injectable({ providedIn: 'root' })
export class PlayerService {}

// AVOID - In module providers (not tree-shakeable)
@NgModule({
  providers: [PlayerService]  // Always included in bundle
})
```

---

## Quick Reference

| Optimization | When to Use |
|--------------|-------------|
| OnPush | All components (default choice) |
| trackBy | All *ngFor with dynamic data |
| Lazy loading | Feature modules, heavy components |
| Virtual scroll | Lists with 100+ items |
| Pure pipes | Formatting, transformations |
| debounceTime | User input (search, filters) |
| distinctUntilChanged | Any value stream that may repeat |