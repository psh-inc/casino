# Bonus Creation Error Fix Documentation

## Issue Description
When creating a bonus, the frontend was getting a 500 Internal Server Error with the message:
```
Cannot deserialize value of type `com.casino.core.domain.ActivationType` from String "NEEDS_CLAIM": 
not one of the values accepted for Enum class: [AUTOMATIC, DEPOSIT_SELECTION, MANUAL_CLAIM]
```

## Root Cause
1. **Enum Mismatch**: The frontend was using different enum values than the backend:
   - Frontend: `NEEDS_CLAIM`, `SELECT_THEN_DEPOSIT`
   - Backend: `MANUAL_CLAIM`, `DEPOSIT_SELECTION`

2. **Request Format**: The frontend was sending the full complex request structure instead of the simplified format expected by the backend.

## Solution Implemented

### 1. Updated Frontend Enums
Changed the `ActivationType` enum in `bonus.service.ts` to match backend values:

```typescript
// Before
export enum ActivationType {
  NEEDS_CLAIM = 'NEEDS_CLAIM',
  AUTOMATIC = 'AUTOMATIC',
  SELECT_THEN_DEPOSIT = 'SELECT_THEN_DEPOSIT'
}

// After
export enum ActivationType {
  MANUAL_CLAIM = 'MANUAL_CLAIM',
  AUTOMATIC = 'AUTOMATIC',
  DEPOSIT_SELECTION = 'DEPOSIT_SELECTION'
}
```

### 2. Updated All References
Updated all references in `bonus-form.component.ts`:
- Changed `NEEDS_CLAIM` → `MANUAL_CLAIM`
- Changed `SELECT_THEN_DEPOSIT` → `DEPOSIT_SELECTION`

### 3. Enhanced Backend Conversion
Improved the `convertToBackendFormat` function to handle missing fields:

```typescript
private convertToBackendFormat(bonus: BonusRequest): any {
  const request: any = {
    code: bonus.bonusCode || bonus.internalName || 'BONUS_' + Date.now(),
    name: bonus.bonusDetails?.[0]?.title || bonus.internalName || 'New Bonus',
    type: this.mapBonusType(bonus.type),
    bonusSubtype: bonus.noDepositSubtype || null,
    description: bonus.bonusDetails?.[0]?.shortDescription || '',
    validFrom: this.formatDateForBackend(bonus.validFrom),
    validTo: this.formatDateForBackend(bonus.validTo),
    autoClaimPriority: bonus.bonusWeight || 0,
    activationType: bonus.activationType || 'AUTOMATIC',
    rewards: [/* ... */]
  };
  return request;
}
```

### 4. Added Response Mapping
Updated `createBonus` to map the backend response to frontend format:

```typescript
createBonus(bonus: BonusRequest): Observable<BonusResponse> {
  const backendRequest = this.convertToBackendFormat(bonus);
  return this.http.post<any>(this.apiUrl, backendRequest).pipe(
    map(backendBonus => this.mapBackendBonusToFrontend(backendBonus))
  );
}
```

## Testing
1. Create a new bonus with any activation type
2. Verify no 500 error occurs
3. Check that the bonus is created successfully
4. Verify the bonus appears in the list with correct data

## Backend Expected Format
The backend expects this simplified structure:
```json
{
  "code": "BONUS_CODE",
  "name": "Bonus Name",
  "type": "DEPOSIT_MATCH",
  "bonusSubtype": null,
  "description": "Description",
  "validFrom": "2025-07-28T10:00:00",
  "validTo": "2025-08-28T10:00:00",
  "autoClaimPriority": 5,
  "activationType": "MANUAL_CLAIM",
  "rewards": [{
    "rewardType": "MONEY",
    "percentageValue": 100,
    "maxAmount": 500,
    "currency": "EUR",
    "wageringMultiplier": 30
  }]
}
```

## Future Considerations
Consider creating a shared constants file between frontend and backend to ensure enum values always match.