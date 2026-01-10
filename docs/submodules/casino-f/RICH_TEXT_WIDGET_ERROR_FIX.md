# Rich Text Widget Error Fix

## Issue

The angular-editor component was throwing an error when trying to access `triggerButtons` property:
```
TypeError: Cannot read properties of undefined (reading 'triggerButtons')
```

## Root Cause

The angular-editor was trying to access its configuration before Angular had properly initialized the component, especially when switching between visual and HTML editing modes.

## Solution

Implemented several fixes to ensure proper initialization:

### 1. Added Editor Ready Flag

Added a `richTextEditorReady` flag to control when the editor is rendered:

```typescript
// Rich Text properties
richTextMode: 'visual' | 'html' = 'visual';
richTextEditorReady = false;
```

### 2. Delayed Initialization

Initialize the editor after a short delay in `ngOnInit`:

```typescript
ngOnInit(): void {
  // ... other initialization
  
  // Initialize Rich Text editor after a short delay
  setTimeout(() => {
    this.richTextEditorReady = true;
  }, 100);
}
```

### 3. Mode Switch Handler

Added a method to properly handle mode switching:

```typescript
onRichTextModeChange(mode: 'visual' | 'html'): void {
  this.richTextMode = mode;
  if (mode === 'visual') {
    // Reset the editor ready flag and reinitialize
    this.richTextEditorReady = false;
    setTimeout(() => {
      this.richTextEditorReady = true;
    }, 100);
  }
}
```

### 4. Template Updates

Updated the template to:
- Only render the editor when ready
- Show a loading state while initializing
- Use proper event binding for mode switching

```html
<!-- Visual Editor Mode -->
<div *ngIf="richTextMode === 'visual' && richTextEditorReady" formGroupName="widgetConfig">
  <angular-editor 
    formControlName="content" 
    [config]="richTextConfig"
    placeholder="Enter your content here..."
    class="rich-text-editor">
  </angular-editor>
</div>
<div *ngIf="richTextMode === 'visual' && !richTextEditorReady" class="editor-loading">
  <mat-spinner diameter="30"></mat-spinner>
  <span>Loading editor...</span>
</div>
```

### 5. Additional Features

Also added:
- CSS class field for custom styling
- Proper form initialization for Rich Text widget
- Loading styles for better UX

## Result

The error is now resolved. The editor properly initializes when:
- First loading the widget edit page
- Switching between visual and HTML modes
- Loading existing widget data

The user sees a brief loading spinner while the editor initializes, preventing any interaction with an uninitialized component.