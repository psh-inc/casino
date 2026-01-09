```markdown
---
name: typescript
description: |
  TypeScript type patterns and strict mode for Angular casino platform.
  Use when: writing Angular services/components, defining models/DTOs, handling RxJS observables, working with API responses.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# TypeScript Skill

This casino platform uses TypeScript across two Angular frontends with different strictness levels. The admin frontend (`casino-f/`) runs with `strict: false` while the customer frontend (`casino-customer-f/`) uses full strict mode. Both require proper typing for services, models, and RxJS observables.

## Quick Start

### Type-Safe Service Pattern

```typescript
@Injectable({ providedIn: 'root' })
export class PlayersService {
  private apiUrl = `${environment.apiUrl}/players`;

  constructor(private http: HttpClient) {}

  // Fully typed with optional parameters
  getPlayerTransactions(
    playerId: number,
    page = 0,
    size = 20,
    type?: TransactionType
  ): Observable<Page<Transaction>> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('size', size.toString());
    if (type) params = params.set('type', type);
    return this.http.get<Page<Transaction>>(`${this.apiUrl}/${playerId}/transactions`, { params });
  }
}
```

### String Literal Enum Pattern

```typescript
// Matches Kotlin backend exactly
export enum PlayerStatus {
  ACTIVE = 'ACTIVE',
  PENDING = 'PENDING',
  SUSPENDED = 'SUSPENDED',
  BLOCKED = 'BLOCKED',
  FROZEN = 'FROZEN'
}

// Exhaustive mapping for UI
export const PLAYER_STATUS_LABELS: Record<PlayerStatus, string> = {
  [PlayerStatus.ACTIVE]: 'Active',
  [PlayerStatus.PENDING]: 'Pending',
  [PlayerStatus.SUSPENDED]: 'Suspended',
  [PlayerStatus.BLOCKED]: 'Blocked',
  [PlayerStatus.FROZEN]: 'Frozen'
};
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Path aliases | Organized imports | `@core/*`, `@shared/*`, `@modules/*` |
| String enums | Backend compatibility | `enum Status { ACTIVE = 'ACTIVE' }` |
| Generic services | Type-safe HTTP | `http.get<Page<T>>()` |
| Literal unions | Restricted values | `view: 'grid' \| 'list'` |
| Partial<T> | PATCH operations | `patchPlayer(id, Partial<Player>)` |
| Record<K, V> | Exhaustive mappings | `Record<Status, string>` |

## Common Patterns

### Observable Cleanup

**When:** Any component subscribing to observables

```typescript
export class ResourceComponent implements OnDestroy {
  private destroy$ = new Subject<void>();

  ngOnInit() {
    this.service.getData().pipe(
      takeUntil(this.destroy$)
    ).subscribe(data => this.data = data);
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

### Generic Dialog Service

**When:** Creating reusable dialog components

```typescript
open<T, D = any, R = any>(
  component: Type<T>,
  config: UiDialogConfig<D> = {}
): UiDialogRef<T, R> {
  const dialogRef = new UiDialogRef<T, R>();
  dialogRef.componentInstance = this.createComponent(component, config.data);
  return dialogRef;
}
```

## See Also

- [patterns](references/patterns.md)
- [types](references/types.md)
- [modules](references/modules.md)
- [errors](references/errors.md)

## Related Skills

- See the **angular** skill for component and service patterns
- See the **jasmine** skill for testing TypeScript code
- See the **kotlin** skill for backend enum/DTO alignment
```