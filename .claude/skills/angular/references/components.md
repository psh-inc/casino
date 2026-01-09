# Angular Component Patterns

## Standalone Component Structure

All components in this project use `standalone: true` (Angular 17 pattern).

```typescript
@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    LoadingSpinnerComponent,
    GameSectionComponent
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HomeComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();
  
  constructor(private gameService: GameService) {}
  
  ngOnInit(): void {
    this.loadGames();
  }
  
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

## Smart vs Presentational Components

### Smart Component (Container)

```typescript
// Handles data fetching, state, business logic
@Component({
  selector: 'app-games-page',
  standalone: true,
  imports: [CommonModule, GameCardComponent],
  template: `
    <app-game-card 
      *ngFor="let game of games$ | async; trackBy: trackByGameId"
      [game]="game"
      (playClick)="onPlayGame(game)">
    </app-game-card>
  `
})
export class GamesPageComponent {
  games$ = this.gameService.getPopularGames();
  
  trackByGameId(index: number, game: Game): string {
    return game.id;
  }
  
  onPlayGame(game: Game): void {
    this.router.navigate(['/games', game.id]);
  }
}
```

### Presentational Component (Dumb)

```typescript
// Pure display, no injected services, OnPush for performance
@Component({
  selector: 'app-game-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './game-card.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class GameCardComponent {
  @Input() game!: Game;
  @Input() isSelected = false;
  
  @Output() playClick = new EventEmitter<void>();
  @Output() favoriteClick = new EventEmitter<void>();
  
  onPlayClick(event: Event): void {
    event.stopPropagation();
    this.playClick.emit();
  }
}
```

## WARNING: Logic in Templates

**The Problem:**

```html
<!-- BAD - Complex logic in template -->
<div *ngIf="user && user.status === 'ACTIVE' && user.balance > 0 && !user.restricted">
  <span>{{ user.balance * exchangeRate | currency }}</span>
</div>
```

**Why This Breaks:**
1. Runs on every change detection cycle
2. Cannot unit test template logic
3. Hard to debug and maintain

**The Fix:**

```typescript
// GOOD - Move to component class
get canPlay(): boolean {
  return this.user?.status === 'ACTIVE' 
    && this.user.balance > 0 
    && !this.user.restricted;
}

get displayBalance(): number {
  return this.user?.balance * this.exchangeRate;
}
```

```html
<div *ngIf="canPlay">
  <span>{{ displayBalance | currency }}</span>
</div>
```

## WARNING: Missing trackBy in ngFor

**The Problem:**

```html
<!-- BAD - No trackBy means full re-render on any change -->
<div *ngFor="let game of games">
  <app-game-card [game]="game"></app-game-card>
</div>
```

**Why This Breaks:**
1. Angular recreates all DOM elements when array reference changes
2. Destroys component state on every update
3. Causes flickering and poor performance

**The Fix:**

```typescript
// Component class
trackByGameId(index: number, game: Game): string {
  return game.id;
}
```

```html
<!-- Template -->
<div *ngFor="let game of games; trackBy: trackByGameId">
  <app-game-card [game]="game"></app-game-card>
</div>
```

## Dependency Injection

```typescript
// Modern inject() function (preferred)
export class GameService {
  private http = inject(HttpClient);
  private router = inject(Router);
}

// Constructor injection (also valid)
export class GameService {
  constructor(
    private http: HttpClient,
    private router: Router
  ) {}
}
```