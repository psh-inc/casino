---
name: angular
description: |
  Angular 17 standalone components, RxJS patterns, reactive forms, and subscription management.
  Use when: Building Angular components, services, guards, interceptors, or working with RxJS observables in casino-f or casino-customer-f.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Angular Skill

This project uses Angular 17 with standalone components across both frontends. The customer frontend (`casino-customer-f`) is fully standalone; the admin frontend (`casino-f`) uses a hybrid approach. All components follow strict subscription cleanup with `takeUntil(destroy$)` and use BehaviorSubject-based state management instead of NgRx.

## Quick Start

### Standalone Component

```typescript
@Component({
  selector: 'app-game-card',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './game-card.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class GameCardComponent implements OnDestroy {
  private destroy$ = new Subject<void>();
  
  @Input() game!: Game;
  @Output() playClick = new EventEmitter<void>();
  
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

### Service with State

```typescript
@Injectable({ providedIn: 'root' })
export class WalletService implements OnDestroy {
  private destroy$ = new Subject<void>();
  private balance$ = new BehaviorSubject<PlayerBalance | null>(null);
  
  getBalance(): Observable<PlayerBalance | null> {
    return this.balance$.asObservable();
  }
  
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
    this.balance$.complete();
  }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Subscription cleanup | `takeUntil(destroy$)` pattern | All 207+ components |
| State containers | BehaviorSubject in services | `AuthService`, `WalletService` |
| Change detection | OnPush for presentational components | `GameCardComponent` |
| Forms | Reactive forms with FormBuilder | `LoginComponent` |
| Guards | Functional guards with `inject()` | `authGuard` |

## Common Patterns

### HTTP Service

```typescript
@Injectable({ providedIn: 'root' })
export class GameService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/api/v1/games`;

  getGames(page = 0, size = 20): Observable<Page<Game>> {
    const params = new HttpParams().set('page', page).set('size', size);
    return this.http.get<Page<Game>>(this.apiUrl, { params }).pipe(
      catchError(error => {
        console.error('Failed to fetch games:', error);
        return throwError(() => error);
      })
    );
  }
}
```

### Functional Guard

```typescript
export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  return authService.isAuthenticated$.pipe(
    map(isAuth => isAuth || router.createUrlTree(['/login']))
  );
};
```

## See Also

- [components](references/components.md)
- [data-fetching](references/data-fetching.md)
- [state](references/state.md)
- [forms](references/forms.md)
- [performance](references/performance.md)

## Related Skills

- See the **typescript** skill for type definitions and interfaces
- See the **jasmine** skill for unit testing Angular components
- See the **playwright** skill for E2E testing