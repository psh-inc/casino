# Game Categories Widget - Live Data Integration

## Overview

The Game Categories widget and CategoryService have been updated to fetch live data from the backend API instead of using mock data. This ensures that category information is always up-to-date and consistent with the backend.

## Changes Made

### 1. CategoryService Updates

#### Updated API Endpoint
- Changed from `/api/v1/categories` to `/api/game-categories` to match the actual backend API

#### Updated Interface
The `GameCategory` interface now matches the backend response:

```typescript
export interface GameCategory {
  id: number;
  name: string;
  code: string;
  description?: string;
  iconUrl?: string;
  bannerUrl?: string;
  mobileIconUrl?: string;
  desktopIconUrl?: string;
  mobileBannerUrl?: string;
  desktopBannerUrl?: string;
  parentId?: number;
  displayOrder: number;
  status: boolean;
  gameCount?: number;
  isRealMoney?: boolean;
  isLiveDealer?: boolean;
}
```

#### Live Data Methods

1. **getCategories(ids?: number[])**
   - Fetches all categories from the backend
   - Filters by specific IDs if provided
   - Returns empty array on error

2. **getAllCategories(topLevelOnly: boolean = true)**
   - New method to fetch categories with top-level filtering
   - Useful for navigation menus

3. **getCategoryById(id: number)**
   - Fetches a single category by ID
   - Uses the dedicated endpoint `/api/game-categories/{id}`

4. **getSubcategories(parentId: number)**
   - New method to fetch subcategories
   - Uses endpoint `/api/game-categories/{parentId}/subcategories`

### 2. Game Categories Widget Updates

#### Enhanced Data Processing
The widget now:
- Properly maps API response fields to component fields
- Handles both legacy field names and new field names (e.g., `iconUrl` and `desktopIconUrl`)
- Determines `isLiveDealer` status based on multiple factors

#### Live Dealer Detection
Since `isLiveDealer` might not always be provided by the API, the widget now determines this based on:
```typescript
const isLiveDealer = cat.isLiveDealer || 
                   cat.code?.toLowerCase().includes('live') || 
                   cat.name?.toLowerCase().includes('live');
```

#### Improved Image Handling
The `getCategoryImage` method now:
- Checks multiple image fields for fallback
- Properly handles carousel vs grid/list layouts
- Supports both old and new API field names

## API Integration

### Endpoints Used

1. **Get Categories**
   - `GET /api/game-categories?topLevelOnly=false`
   - Returns all active categories

### Error Handling

- All API calls include proper error handling
- Returns empty arrays/null on error to prevent UI crashes
- Errors are logged via LoggerService

## Benefits

1. **Real-time Data**: Categories are always current from the database
2. **Consistency**: Frontend displays exactly what's configured in the backend
3. **Flexibility**: Supports filtering and subcategory fetching
4. **Backward Compatibility**: Handles both old and new API response formats
5. **Performance**: Removed unnecessary mock data loading

## Testing Considerations

When testing:
1. Ensure the backend is running and accessible
2. Verify categories are properly configured in the admin panel
3. Check that custom images and names are applied correctly
4. Test with different category configurations (with/without custom data)
5. Verify error handling when API is unavailable

## Future Enhancements

1. Add caching to reduce API calls
2. Implement retry logic for failed requests
3. Add loading states for better UX
4. Support for real-time updates via WebSocket