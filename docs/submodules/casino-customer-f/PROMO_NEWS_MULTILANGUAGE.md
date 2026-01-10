# Promo News Widget - Multilanguage Support

## Overview

Added multilanguage support to the Promo News widget, allowing all text fields to use translation keys that are resolved based on the user's locale.

## Implementation Details

### Frontend Admin Changes

#### 1. Widget Edit Form Updates

Added translation key selector to all text fields in the promo news widget configuration:

```html
<!-- Main widget title -->
<input matInput 
       formControlName="title"
       placeholder="Enter widget title"
       appTranslationKeySelector
       (translationKeyInserted)="onTranslationKeyInserted($event, 'title')">

<!-- Promo news item fields -->
<input matInput 
       [(ngModel)]="item.title"
       placeholder="Title"
       appTranslationKeySelector
       (translationKeyInserted)="onPromoNewsTranslationKeyInserted(i, 'title', $event)">
```

#### 2. Supported Fields

All the following fields now support translation keys:
- Widget title
- Item title
- Item subtitle  
- Item read more label
- Item CTA label

### Backend Translation Resolution

#### TranslationResolutionService Updates

```kotlin
private fun resolvePromoNewsWidget(content: Any, translations: Map<String, String>): Any {
    return when (content) {
        is Map<*, *> -> {
            val mutableContent = content.toMutableMap()
            
            // Resolve widget title
            content["title"]?.toString()?.let { title ->
                mutableContent["title"] = replaceTranslationKeysInText(title, translations)
            }
            
            // Resolve items
            (content["items"] as? List<*>)?.let { items ->
                mutableContent["items"] = items.map { item ->
                    when (item) {
                        is Map<*, *> -> {
                            val mutableItem = item.toMutableMap()
                            // Resolve all text fields
                            item["title"]?.toString()?.let { 
                                mutableItem["title"] = replaceTranslationKeysInText(it, translations)
                            }
                            // ... similar for subtitle, readMoreLabel, ctaLabel
                            mutableItem
                        }
                        else -> item
                    }
                }
            }
            
            mutableContent
        }
        else -> content
    }
}
```

## Usage

### Admin Panel

1. When editing a promo news widget, click on any text field
2. Type `{` or press `Ctrl+Space` to open the translation key selector
3. Select or type a translation key (e.g., `promo.winter.title`)
4. The field will contain: `{promo.winter.title}`

### Customer Portal

The translation keys are automatically resolved based on:
- User's selected language
- Available translations in the system
- Fallback to empty string if translation not found

### Example Configuration

```json
{
  "widgetType": "promo_news",
  "widgetConfig": {
    "title": "{promo.news.section.title}",
    "items": [
      {
        "title": "{promo.winter.bonus.title}",
        "subtitle": "Get 50% bonus - {promo.winter.bonus.subtitle}",
        "readMoreLabel": "{common.read.more}",
        "ctaLabel": "{common.claim.now}"
      }
    ]
  }
}
```

## Benefits

1. **Consistency**: Same translation pattern as other widgets
2. **Flexibility**: Mix static text with translation keys
3. **Maintainability**: Centralized translation management
4. **User Experience**: Seamless multilanguage support for global audiences