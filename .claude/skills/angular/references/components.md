# Angular Component Patterns

## Standalone Components

All new components in this codebase MUST be standalone. The customer frontend uses standalone exclusively.

### Basic Structure

```typescript
@Component({
  selector: 'app-game-card',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    TranslateModule
  ],
  templateUrl: './game-card.component.html',
  styleUrl: './game-card.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class GameCardComponent {
  @Input({ required: true }) game!: GameDto;
  @Output() favorite = new EventEmitter<string>();

  onFavoriteClick(event: Event): void {
    event.stopPropagation();
    this.favorite.emit(this.game.id);
  }
}
```

### Complex Component with State

```typescript
@Component({
  selector: 'app-games-list-widget',
  standalone: true,
  imports: [CommonModule, GameCardComponent, InfiniteScrollModule],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class GamesListComponent implements OnInit, OnDestroy {
  @Input() widget!: ResolvedWidget;

  displayedGames: GameDto[] = [];
  currentOffset = 0;
  pageSize = 20;
  hasMoreGames = false;
  isLoadingMore = false;

  private destroy$ = new Subject<void>();

  constructor(
    private gameService: GameService,
    private favoritesService: FavoritesService
  ) {}

  ngOnInit(): void {
    if (this.widget?.content?.games) {
      this.displayedGames = this.widget.content.games;
      this.currentOffset = this.displayedGames.length;
      this.hasMoreGames = this.currentOffset < (this.widget.content.totalCount || 0);
    }
  }

  loadMoreGames(): void {
    if (this.isLoadingMore || !this.hasMoreGames) return;

    this.isLoadingMore = true;
    this.gameService.getGames({}, {}, this.pageSize, this.currentOffset).pipe(
      takeUntil(this.destroy$),
      finalize(() => this.isLoadingMore = false)
    ).subscribe({
      next: (response) => {
        this.displayedGames = [...this.displayedGames, ...response.games];
        this.currentOffset += response.games.length;
        this.hasMoreGames = this.currentOffset < response.total;
      },
      error: (error) => console.error('Failed to load games:', error)
    });
  }

  trackByGameId(index: number, game: GameDto): string {
    return game.id;
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

---

## WARNING: Logic in Templates

**The Problem:**

```html
<!-- BAD - Complex logic in template -->
<div *ngIf="user && user.kycStatus === 'VERIFIED' && user.balance > minWithdrawal && !user.withdrawalsRestricted">
  <button (click)="withdraw()">Withdraw</button>
</div>
```

**Why This Breaks:**
1. Impossible to unit test template conditions
2. Re-evaluated on every change detection cycle
3. Duplicated if same logic needed elsewhere
4. Hard to read and maintain

**The Fix:**

```typescript
// GOOD - Logic in component class
get canWithdraw(): boolean {
  return this.user?.kycStatus === 'VERIFIED' 
    && (this.user?.balance ?? 0) > this.minWithdrawal
    && !this.user?.withdrawalsRestricted;
}
```

```html
<!-- Clean template -->
<div *ngIf="canWithdraw">
  <button (click)="withdraw()">Withdraw</button>
</div>
```

---

## WARNING: Using `any` Type

**The Problem:**

```typescript
// BAD - Defeats TypeScript benefits
@Input() data: any;
games: any[] = [];
```

**Why This Breaks:**
1. No autocomplete or type checking
2. Runtime errors instead of compile-time errors
3. Impossible to refactor safely
4. Documentation is lost

**The Fix:**

```typescript
// GOOD - Proper interfaces
interface GameDto {
  id: string;
  name: string;
  provider: string;
  isFavorite: boolean;
}

@Input() data!: GameDto;
games: GameDto[] = [];
```

---

## Input/Output Patterns

### Required Inputs (Angular 17+)

```typescript
@Input({ required: true }) playerId!: number;
@Input() showDetails = false;  // Optional with default
```

### Output Events

```typescript
@Output() gameSelected = new EventEmitter<GameDto>();
@Output() filterChanged = new EventEmitter<FilterState>();

onGameClick(game: GameDto): void {
  this.gameSelected.emit(game);
}
```

---

## Optimistic Updates Pattern

Used for favorite toggling in this codebase:

```typescript
toggleFavorite(game: GameDto, event: Event): void {
  event.stopPropagation();
  if (this.favoriteLoadingId === game.id) return;

  this.favoriteLoadingId = game.id;
  const currentStatus = game.isFavorite;
  game.isFavorite = !currentStatus;  // Optimistic update

  this.favoritesService.toggleFavorite(game.id, currentStatus).subscribe({
    next: (response) => {
      if (!response.success) {
        game.isFavorite = currentStatus;  // Revert on failure
      }
      this.favoriteLoadingId = null;
    },
    error: () => {
      game.isFavorite = currentStatus;  // Revert on error
      this.favoriteLoadingId = null;
    }
  });
}
```

---

## Dialog/Modal Pattern

```typescript
openCashier(): void {
  this.paymentService.initiatePaymentSession().pipe(
    takeUntil(this.destroy$)
  ).subscribe({
    next: (session) => {
      const dialogRef = this.dialog.open(CashierModalComponent, {
        data: { cashierUrl: session.cashierUrl },
        width: '600px',
        disableClose: true
      });

      dialogRef.afterClosed().subscribe(result => {
        if (result?.success) {
          this.walletService.refreshWalletSummary().subscribe();
        }
      });
    }
  });
}
```

---

## File Naming Convention

| Type | Convention | Example |
|------|------------|---------|
| Component | kebab-case | `game-card.component.ts` |
| Service | kebab-case | `games.service.ts` |
| Model | kebab-case | `game.model.ts` |
| Guard | kebab-case | `auth.guard.ts` |
| Interceptor | kebab-case | `error.interceptor.ts` |