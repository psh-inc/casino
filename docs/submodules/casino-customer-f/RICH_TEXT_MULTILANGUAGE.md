# Rich Text Widget - Multilanguage Support

## Overview

Added multilanguage support to the Rich Text widget, allowing HTML content to include translation keys that are resolved based on the user's locale.

## Implementation Details

### Admin Frontend Features

#### Editor Modes

The Rich Text widget now supports two editing modes:

1. **Visual Editor Mode** - WYSIWYG editing using angular-editor
2. **HTML Mode** - Direct HTML editing with translation key support

Users can toggle between modes using the mode selector buttons.

#### Translation Key Support in HTML Mode

When in HTML mode, users can:
- Type `{` or press `Ctrl+Space` to insert translation keys
- Mix HTML content with translation keys
- Example: `<h1>{welcome.title}</h1><p>{welcome.message}</p>`

### Backend Translation Resolution

#### RichTextWidgetContent DTO

```kotlin
@JsonInclude(JsonInclude.Include.NON_NULL)
data class RichTextWidgetContent(
    val content: String? = null,      // Rich text/HTML content
    val sanitize: Boolean = true,     // Whether to sanitize the HTML (default true for safety)
    val cssClass: String? = null      // Optional CSS class for styling
)
```

#### Translation Resolution

The `resolveRichTextWidget` method supports both Map and DTO representations:
- Resolves translation keys in the content field
- Preserves sanitize and cssClass settings
- Supports all translation key patterns: `{key}`, `[[key]]`, `{{key}}`

### Customer Frontend Widget

Created a dedicated Rich Text widget component that:
- Displays resolved HTML content
- Applies the translation pipe for any remaining keys
- Handles content sanitization based on configuration
- Supports custom CSS classes

## Usage Examples

### Admin Panel

1. Select "RICH_TEXT" widget type
2. Toggle to "HTML Mode" for translation support
3. Enter content with translation keys:
   ```html
   <div class="welcome-section">
     <h2>{home.welcome.title}</h2>
     <p>{home.welcome.description}</p>
     <button class="btn">{common.learn.more}</button>
   </div>
   ```

### Configuration Example

```json
{
  "widgetType": "RICH_TEXT",
  "widgetConfig": {
    "content": "<h1>{promo.title}</h1><p>{promo.description}</p>",
    "sanitize": true,
    "cssClass": "highlight"
  }
}
```

### Customer Display

The widget will:
1. Resolve translation keys server-side
2. Apply any remaining translations client-side
3. Sanitize content if enabled
4. Apply custom CSS class if specified

## Security Features

- **Content Sanitization**: Enabled by default to prevent XSS attacks
- **Safe HTML Rendering**: Uses Angular's DomSanitizer
- **Configurable**: Can disable sanitization for trusted content

## Styling

The Rich Text widget includes comprehensive styles for:
- Typography (headings, paragraphs, lists)
- Links with hover effects
- Code blocks and inline code
- Tables with hover states
- Blockquotes with special styling
- Images with responsive sizing
- Custom button styles

## Benefits

1. **Flexibility**: Switch between visual and HTML editing
2. **Multilanguage**: Full translation key support
3. **Security**: Built-in content sanitization
4. **Customization**: Support for custom CSS classes
5. **Rich Formatting**: Complete HTML content support