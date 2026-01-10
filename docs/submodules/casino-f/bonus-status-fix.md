# Bonus Status Fix Documentation

## Issue Description
When creating a bonus with the "Active" checkbox selected, the bonus was always being created as "DRAFT" instead of "ACTIVE".

## Root Cause
The backend Bonus entity has a default status of `DRAFT`:
```kotlin
@Column(nullable = false, length = 20)
val status: BonusStatus = BonusStatus.DRAFT
```

The `CreateBonusRequest` DTO doesn't include a status field, so all bonuses are created with the default DRAFT status.

## Solution Implemented
Modified the bonus creation flow to:
1. Create the bonus (which will be DRAFT by default)
2. If the user selected "Active", immediately activate the bonus using the activate endpoint

### Updated createBonus Method
```typescript
createBonus(bonus: BonusRequest): Observable<BonusResponse> {
  const backendRequest = this.convertToBackendFormat(bonus);
  
  // Create the bonus first (it will be created as DRAFT)
  return this.http.post<any>(this.apiUrl, backendRequest).pipe(
    map(backendBonus => this.mapBackendBonusToFrontend(backendBonus)),
    switchMap(createdBonus => {
      // If the user wants the bonus to be active, activate it
      if (bonus.isActive) {
        return this.activateBonus(createdBonus.id).pipe(
          map(activatedBonus => this.mapBackendBonusToFrontend(activatedBonus))
        );
      }
      // Otherwise, return the draft bonus
      return of(createdBonus);
    })
  );
}
```

### Also Updated
- `activateBonus` method to properly map backend response
- `deactivateBonus` method to properly map backend response

## How It Works
1. User fills out bonus form and checks "Active" checkbox
2. Frontend sends the creation request
3. Backend creates bonus as DRAFT
4. If `isActive` is true, frontend immediately calls activate endpoint
5. Backend updates status to ACTIVE
6. User sees the bonus created with ACTIVE status

## Testing
1. Create a new bonus with "Active" checkbox checked
2. After creation, verify the bonus shows as "Active" in the list
3. Create a new bonus with "Active" checkbox unchecked
4. After creation, verify the bonus shows as "Draft" in the list

## Alternative Solution (Backend)
A cleaner solution would be to modify the backend to:
- Accept a `status` field in `CreateBonusRequest`
- Allow setting initial status during creation
- This would eliminate the need for two API calls