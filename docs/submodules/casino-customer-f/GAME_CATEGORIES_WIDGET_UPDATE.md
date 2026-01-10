# Game Categories Widget Update - Customer Frontend

## Overview

The Game Categories widget component has been updated to support custom names, descriptions, and responsive images from the widget configuration. This allows the widget to display category-specific overrides provided by the CMS.

## Changes Made

### 1. Interface Updates

Updated the `GameCategoriesWidgetContent` interface to include custom name and description fields:

```typescript
customCategoryImages?: {
  [key: string]: {
    desktopIconUrl?: string;
    desktopBannerUrl?: string;
    mobileIconUrl?: string;
    mobileBannerUrl?: string;
    customName?: string;         // New field
    customDescription?: string;   // New field
  }
};
```

### 2. Data Processing

The `loadCategories` method now applies custom data to each category:

```typescript
// Apply custom images, names, and descriptions if provided
const categoriesWithCustomData = categories.map(cat => {
  const customData = widgetContent.customCategoryImages?.[cat.id.toString()];
  if (customData) {
    return {
      ...cat,
      iconUrl: customData.desktopIconUrl || cat.iconUrl,
      bannerUrl: customData.desktopBannerUrl || cat.bannerUrl,
      name: customData.customName || cat.name,
      description: customData.customDescription || cat.description,
      mobileIconUrl: customData.mobileIconUrl,
      mobileBannerUrl: customData.mobileBannerUrl
    };
  }
  return cat;
});
```

### 3. Responsive Image Support

The `getCategoryImage` method now checks for mobile-specific images:

```typescript
getCategoryImage(category: any): string {
  // Check for mobile images on mobile devices
  if (this.isMobile) {
    if (this.content?.layout === 'carousel' && category.mobileBannerUrl) {
      return category.mobileBannerUrl;
    }
    if (category.mobileIconUrl) {
      return category.mobileIconUrl;
    }
  }
  
  // Use iconUrl for grid/list layouts, bannerUrl for carousel
  if (this.content?.layout === 'carousel' && category.bannerUrl) {
    return category.bannerUrl;
  }
  return category.iconUrl || '/assets/images/default-category.png';
}
```

## Configuration Example

Based on the provided configuration, the widget will now properly use:

```json
{
  "type": "GAME_CATEGORIES",
  "content": {
    "customCategoryImages": {
      "2": {
        "desktopIconUrl": "https://example.com/icon.png",
        "desktopBannerUrl": "https://example.com/banner.png",
        "customName": "Table Games"  // This will override the default category name
      }
    }
  }
}
```

## Features

1. **Custom Names**: Categories can display custom names instead of their default names
2. **Custom Descriptions**: Categories can have custom descriptions
3. **Responsive Images**: Different images for mobile and desktop
4. **Fallback Logic**: Falls back to default values if custom values are not provided
5. **Translation Support**: Custom names and descriptions support translation keys (resolved by backend)

## User Experience

- When viewing category ID 2, users will see "Table Games" instead of the default category name
- Mobile users will see mobile-optimized images if provided
- All custom text is resolved by the backend translation service

## Testing

The widget has been tested with:
- Custom names and descriptions
- Mobile and desktop image variations
- Different layout modes (grid, list, carousel)
- Fallback scenarios when custom data is not provided

## Notes

- The HTML template doesn't need changes as it already uses `{{ category.name }}` and `{{ category.description }}`
- The component maintains backward compatibility with configurations that don't include custom data
- Mobile detection is based on viewport width (< 768px)