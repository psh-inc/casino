# Angular Performance Patterns

## Change Detection Strategy

### OnPush for Presentational Components

```typescript
// GOOD - OnPush reduces change detection cycles
@Component({
  selector: 'app-game-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './game-card.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class GameCardComponent {
  @Input() game!: Game;
  @Output() playClick = new EventEmitter<void>();
}
```

### WARNING: OnPush with Mutable State

**The Problem:**

```typescript
// BAD - Mutating object doesn't trigger change detection with OnPush
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BadComponent {
  user = { name: 'John', balance: 100 };
  
  updateBalance(): void {
    this.user.balance = 200; // View won't update!
  }
}
```

**Why This Breaks:**
1. OnPush only checks reference equality
2. Object mutation keeps same reference
3. View becomes stale

**The Fix:**

```typescript
// GOOD - Create new object reference
updateBalance(): void {
  this.user = { ...this.user, balance: 200 };
}

// OR use ChangeDetectorRef
constructor(private cdr: ChangeDetectorRef) {}

updateBalance(): void {
  this.user.balance = 200;
  this.cdr.markForCheck();
}
```

## trackBy in ngFor

```typescript
// Always use trackBy for lists
@Component({
  template: `
    <div *ngFor="let game of games; trackBy: trackByGameId">
      <app-game-card [game]="game"></app-game-card>
    </div>
  `
})
export class GamesListComponent {
  trackByGameId(index: number, game: Game): string {
    return game.id;
  }
}
```

**Statistics from this codebase:**
- 207+ components
- Only ~5 components use OnPush explicitly
- trackBy is used consistently in lists

## WARNING: Computed Values in Templates

**The Problem:**

```html
<!-- BAD - Method called on every change detection -->
<div>{{ calculateTotal() }}</div>
<div>{{ formatDate(item.date) }}</div>
```

**Why This Breaks:**
1. Methods called on every change detection cycle
2. Can run dozens of times per second
3. Expensive operations kill performance

**The Fix:**

```typescript
// GOOD - Use getters or pipes
get total(): number {
  return this.items.reduce((sum, item) => sum + item.price, 0);
}

// OR use pure pipe
@Pipe({ name: 'formatDate', pure: true })
export class FormatDatePipe implements PipeTransform {
  transform(value: Date): string {
    return format(value, 'yyyy-MM-dd');
  }
}
```

## Lazy Loading Routes

```typescript
// app.routes.ts
export const routes: Routes = [
  {
    path: 'games',
    loadChildren: () => import('./features/games/games.routes')
      .then(m => m.GAMES_ROUTES)
  },
  {
    path: 'wallet',
    loadComponent: () => import('./features/wallet/wallet.component')
      .then(m => m.WalletComponent)
  }
];
```

## Async Pipe vs Manual Subscription

```typescript
// GOOD - Async pipe handles subscription and cleanup
@Component({
  template: `
    <div *ngIf="user$ | async as user">
      {{ user.name }}
    </div>
  `
})
export class UserComponent {
  user$ = this.userService.getCurrentUser();
}

// AVOID - Manual subscription requires cleanup
@Component({...})
export class BadComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();
  user: User | null = null;
  
  ngOnInit(): void {
    this.userService.getCurrentUser().pipe(
      takeUntil(this.destroy$)
    ).subscribe(user => this.user = user);
  }
  
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

The async pipe is preferred when you only need to display the value. Use manual subscription when you need to perform side effects.

## Bundle Optimization

```bash
# Analyze bundle size
ng build --configuration production --stats-json
npx webpack-bundle-analyzer dist/stats.json
```