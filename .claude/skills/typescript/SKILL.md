```markdown
---
name: typescript
description: |
  TypeScript 5.2+ type patterns and strict mode for Angular casino platform.
  Use when: Writing TypeScript code in casino-f/, casino-customer-f/, or casino-shared/.
  Working with interfaces, enums, generics, or RxJS observables.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# TypeScript Skill

TypeScript 5.2+ type patterns for the casino platform's Angular frontends and shared library. The codebase uses varying strictness levels: `casino-shared/` enforces full strict mode, `casino-customer-f/` uses `strict: true`, while `casino-f/` uses selective strict checks for development flexibility.

## Quick Start

### String Enums

```typescript
// Standard pattern for status/type enums
export enum BonusStatus {
  DRAFT = 'DRAFT',
  ACTIVE = 'ACTIVE',
  INACTIVE = 'INACTIVE',
  EXPIRED = 'EXPIRED'
}
```

### Generic Page Interface

```typescript
export interface Page<T> {
  content: T[];
  totalElements: number;
  totalPages: number;
  size: number;
  number: number;
  first: boolean;
  last: boolean;
}
```

### Service with Typed Observables

```typescript
@Injectable({ providedIn: 'root' })
export class PlayerService {
  constructor(private http: HttpClient) {}

  getPlayers(page = 0, size = 20): Observable<Page<Player>> {
    const params = new HttpParams()
      .set('page', page.toString())
      .set('size', size.toString());
    return this.http.get<Page<Player>>(`${environment.apiUrl}/players`, { params });
  }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| String Enums | Status values, types | `enum GameType { SLOTS = 'SLOTS' }` |
| Interfaces | Data models, DTOs | `interface Player { id: number; }` |
| Generics | Pagination, collections | `Page<T>`, `Map<string, T>` |
| Union Types | Mutually exclusive values | `type: 'BONUS' \| 'DEPOSIT'` |
| Mapped Types | Display labels | `Record<GameType, string>` |
| Path Aliases | Clean imports | `@core/*`, `@shared/*` |

## Common Patterns

### BehaviorSubject for State

**When:** Managing component or service state that needs immediate values

```typescript
private isLoadingSubject = new BehaviorSubject<boolean>(false);
public isLoading$ = this.isLoadingSubject.asObservable();

// Get current value synchronously
const loading = this.isLoadingSubject.value;
```

### Mapped Type for Labels

**When:** Displaying enum values in UI

```typescript
export const GAME_TYPE_LABELS: Record<GameType, string> = {
  [GameType.SLOTS]: 'Slots',
  [GameType.TABLE_GAMES]: 'Table Games',
  [GameType.LIVE_CASINO]: 'Live Casino'
};
```

## See Also

- [patterns](references/patterns.md)
- [types](references/types.md)
- [modules](references/modules.md)
- [errors](references/errors.md)

## Related Skills

- See the **angular** skill for component and service patterns
- See the **jpa** skill for backend entity types that mirror frontend interfaces
```