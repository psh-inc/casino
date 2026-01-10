# Bonus List Display Fix Documentation

## Issue Description
The bonus list page was not displaying bonus titles and codes properly. The columns were empty even though other data was being loaded.

## Root Cause
The backend API returns bonuses with these field names:
- `code` - The bonus code
- `name` - The bonus name/title
- `description` - The bonus description

However, the frontend expected these field names:
- `bonusCode` - For the code
- `bonusDetails` - An array containing title and descriptions

## Solution Implemented

### 1. Created a Mapping Function
Added `mapBackendBonusToFrontend()` method in `bonus.service.ts` that maps backend fields to frontend interface:

```typescript
private mapBackendBonusToFrontend(backendBonus: any): BonusResponse {
  return {
    // Maps backend 'code' to frontend 'bonusCode'
    bonusCode: backendBonus.code || '',
    
    // Maps backend 'code' to frontend 'internalName'
    internalName: backendBonus.code || backendBonus.internalName || '',
    
    // Creates bonusDetails array from backend 'name' and 'description'
    bonusDetails: [{
      language: 'en',
      title: backendBonus.name || backendBonus.code || 'Bonus',
      shortDescription: backendBonus.description || '',
      detailedDescription: backendBonus.description || '',
      bannerUrl: ''
    }],
    
    // ... other field mappings
  };
}
```

### 2. Updated getBonuses Method
Modified the `getBonuses()` method to apply the mapping to all bonuses in the list:

```typescript
getBonuses(page = 0, size = 20, status?: BonusStatus): Observable<Page<BonusResponse>> {
  return this.http.get<Page<any>>(this.apiUrl, { params }).pipe(
    map(response => {
      const mappedContent = response.content.map((backendBonus: any) => 
        this.mapBackendBonusToFrontend(backendBonus)
      );
      
      return {
        ...response,
        content: mappedContent
      } as Page<BonusResponse>;
    })
  );
}
```

### 3. Unified Mapping Across All Methods
- `getBonusById()` - Now uses the same mapping function
- `getAllBonusesForCopy()` - Updated to use the mapping function

## How the Fix Works

1. **Backend Returns**: 
   ```json
   {
     "id": 1,
     "code": "WELCOME100",
     "name": "Welcome Bonus 100%",
     "description": "100% match on first deposit",
     "status": "ACTIVE",
     ...
   }
   ```

2. **Frontend Receives** (after mapping):
   ```json
   {
     "id": 1,
     "bonusCode": "WELCOME100",
     "internalName": "WELCOME100",
     "bonusDetails": [{
       "language": "en",
       "title": "Welcome Bonus 100%",
       "shortDescription": "100% match on first deposit",
       ...
     }],
     "status": "ACTIVE",
     ...
   }
   ```

3. **Template Displays**:
   - Code column: Shows `bonus.bonusCode`
   - Name column: Shows `getBonusTitle(bonus)` which reads from `bonus.bonusDetails[0].title`

## Testing
After applying this fix:
1. Navigate to the Bonuses page
2. All bonuses should display with:
   - Proper codes in the Code column
   - Proper titles in the Name column
   - Descriptions visible under the title
3. Search functionality should work with bonus codes and titles
4. Edit and Apply from existing features should work correctly

## Future Considerations
Consider updating either:
1. The backend to return data in the format the frontend expects, OR
2. The frontend interfaces to match the backend response format

This would eliminate the need for mapping and reduce potential bugs.