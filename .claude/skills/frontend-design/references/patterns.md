# Patterns Reference

Design anti-patterns, best practices, and visual consistency guidelines.

## WARNING: Prop Drilling Styles

**The Problem:**

```typescript
// BAD - Passing style values through component tree
@Component({
  template: `
    <app-card [backgroundColor]="'#1a1a2e'" [borderRadius]="'12px'" [padding]="'16px'">
      <app-header [fontSize]="'18px'" [fontWeight]="'bold'">...</app-header>
    </app-card>
  `
})
```

**Why This Breaks:**
1. Inconsistency - Each instance can have different values
2. Maintenance nightmare - Updates require changing every call site
3. No type safety - String-based values can have typos

**The Fix:**

```typescript
// GOOD - Use variant-based components
@Component({
  template: `
    <ui-card variant="elevated" padding="md">
      <ui-card-header>...</ui-card-header>
    </ui-card>
  `
})
```

## WARNING: Inline Object Styles

**The Problem:**

```typescript
// BAD - Creating new style objects in template
@Component({
  template: `
    <div [ngStyle]="{ backgroundColor: getColor(), padding: '16px' }">
      ...
    </div>
  `
})
```

**Why This Breaks:**
1. New object reference every render - Triggers change detection
2. Performance hit - Especially in large lists
3. Bypasses design system

**The Fix:**

```typescript
// GOOD - Use CSS classes or cached styles
@Component({
  template: `
    <div [ngClass]="cardClasses">...</div>
  `
})
export class CardComponent {
  cardClasses = computed(() => ({
    'bg-primary': this.variant() === 'primary',
    'p-4': true
  }));
}
```

## WARNING: Magic Colors

**The Problem:**

```scss
// BAD - Hardcoded hex values scattered through code
.header { background: #0A1E26; }
.sidebar { background: #0B2029; }
.card { background: #0C2230; }  // Slightly different each time
```

**Why This Breaks:**
1. Brand inconsistency - Similar but not identical colors
2. Impossible to theme - Can't change globally
3. No semantic meaning - What does #0C2230 represent?

**The Fix:**

```scss
// GOOD - Use design tokens
.header { background: $color-primary; }
.sidebar { background: $color-background-elevated; }
.card { background: $color-surface; }
```

## WARNING: Missing Focus States

**The Problem:**

```scss
// BAD - Removing focus outline without replacement
button:focus {
  outline: none;  // Accessibility violation
}
```

**Why This Breaks:**
1. Keyboard users can't see focus - Can't navigate
2. Accessibility failure - WCAG 2.4.7 violation
3. Legal risk - ADA compliance issues

**The Fix:**

```scss
// GOOD - Custom focus ring
button {
  &:focus {
    outline: none;
  }
  
  &:focus-visible {
    box-shadow: 0 0 0 3px rgba(58, 166, 96, 0.4);  // Casino green ring
  }
}

// Or use Tailwind
.button {
  @apply focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2;
}
```

## WARNING: Inconsistent Border Radius

**The Problem:**

```scss
// BAD - Random radius values
.card { border-radius: 8px; }
.button { border-radius: 6px; }
.input { border-radius: 4px; }
.modal { border-radius: 12px; }
.badge { border-radius: 3px; }
```

**Why This Breaks:**
1. Visual inconsistency - Elements don't feel cohesive
2. Maintenance burden - Hard to update systematically
3. Design debt - Accumulates over time

**The Fix:**

```scss
// GOOD - Use radius scale
$radius-sm: 4px;   // Small elements: badges, chips
$radius-md: 8px;   // Interactive: buttons, inputs
$radius-lg: 12px;  // Containers: cards, modals
$radius-xl: 16px;  // Large containers: sections
$radius-full: 9999px;  // Pills, avatars

.card { border-radius: $radius-lg; }
.button { border-radius: $radius-md; }
.input { border-radius: $radius-md; }
.modal { border-radius: $radius-lg; }
.badge { border-radius: $radius-sm; }
```

## WARNING: Text Truncation Without Tooltip

**The Problem:**

```scss
// BAD - Hiding content without disclosure
.game-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

**Why This Breaks:**
1. Lost information - Users can't see full title
2. Frustration - No way to access hidden content
3. Accessibility issue - Screen readers may or may not read full text

**The Fix:**

```typescript
// GOOD - Truncate with tooltip
@Component({
  template: `
    <span 
      class="game-title truncate" 
      [title]="fullTitle"
      [attr.aria-label]="fullTitle">
      {{ displayTitle }}
    </span>
  `
})
export class GameCardComponent {
  displayTitle = computed(() => 
    this.game().title.length > 20 
      ? this.game().title.slice(0, 20) + '...' 
      : this.game().title
  );
  fullTitle = computed(() => this.game().title);
}
```

## Do: Component Composition

```typescript
// GOOD - Compose small, focused components
@Component({
  template: `
    <ui-card variant="default">
      <ui-card-header>
        <ui-badge variant="success">Active</ui-badge>
        <span>Player Details</span>
      </ui-card-header>
      <ui-card-content>
        <ui-form-field label="Username">
          <ui-input formControlName="username"></ui-input>
        </ui-form-field>
      </ui-card-content>
      <ui-card-footer>
        <ui-button variant="ghost">Cancel</ui-button>
        <ui-button variant="primary">Save</ui-button>
      </ui-card-footer>
    </ui-card>
  `
})
```

## Do: Responsive-First Development

```scss
// GOOD - Mobile-first with progressive enhancement
.game-grid {
  // Base: Mobile
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  
  // Tablet up
  @media (min-width: 768px) {
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
  }
  
  // Desktop up
  @media (min-width: 1280px) {
    grid-template-columns: repeat(6, 1fr);
    gap: 1.25rem;
  }
}
```

## Do: Semantic Color Usage

```scss
// GOOD - Colors have meaning
$color-success: #4caf50;   // Positive actions, confirmations
$color-warning: #ff9800;   // Caution, pending states
$color-danger: #f44336;    // Destructive actions, errors
$color-info: #2196f3;      // Informational, neutral

// Usage
.status-active { color: $color-success; }
.status-pending { color: $color-warning; }
.status-blocked { color: $color-danger; }
```

## Custom Scrollbar

```scss
// Consistent scrollbar styling
@mixin custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
  
  &::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    
    &:hover {
      background: rgba(255, 255, 255, 0.3);
    }
  }
  
  &::-webkit-scrollbar-track {
    background: transparent;
  }
}
```