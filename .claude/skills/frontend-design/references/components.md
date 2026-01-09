# Components Reference

UI component styling patterns and composition for Angular standalone components.

## Component Architecture

### Admin Frontend UI Library

Located in `casino-f/src/app/shared/ui/`, all components follow this pattern:

| Component | Selector | Purpose |
|-----------|----------|---------|
| Button | `ui-button` | Actions with 7 variants |
| Card | `ui-card` | Content containers |
| Form Field | `ui-form-field` | Label + validation |
| Input | `ui-input` | Text input |
| Modal | `ui-modal` | Dialog windows |
| Toast | `ui-toast` | Notifications |
| Badge | `ui-badge` | Status indicators |

### Button Component Pattern

```typescript
// casino-f/src/app/shared/ui/ui-button.component.ts
export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger' | 'outline' | 'success' | 'warning';
export type ButtonSize = 'xs' | 'sm' | 'md' | 'lg' | 'icon';

@Component({
  selector: 'ui-button',
  standalone: true,
  imports: [CommonModule, UiIconComponent],
  template: `
    <button [ngClass]="buttonClasses()" [disabled]="disabled()" [type]="type()">
      <ui-icon *ngIf="iconLeft()" [name]="iconLeft()" [size]="iconSize()"></ui-icon>
      <ng-content></ng-content>
      <ui-icon *ngIf="iconRight()" [name]="iconRight()" [size]="iconSize()"></ui-icon>
    </button>
  `
})
export class UiButtonComponent {
  variant = input<ButtonVariant>('primary');
  size = input<ButtonSize>('md');
  disabled = input<boolean>(false);

  buttonClasses = computed(() => {
    const base = 'inline-flex items-center justify-center gap-2 font-semibold transition-all rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-60';
    
    const variants = {
      primary: 'bg-primary-600 text-white shadow-sm hover:bg-primary-700 focus:ring-primary-500',
      secondary: 'bg-slate-100 text-slate-900 shadow-sm hover:bg-slate-200',
      ghost: 'bg-transparent text-slate-700 hover:bg-slate-100',
      danger: 'bg-danger-600 text-white shadow-sm hover:bg-danger-700'
    };
    
    const sizes = {
      xs: 'text-xs px-2 py-1',
      sm: 'text-xs px-3 py-1.5',
      md: 'text-sm px-4 py-2',
      lg: 'text-base px-5 py-2.5',
      icon: 'p-2'
    };

    return `${base} ${variants[this.variant()]} ${sizes[this.size()]}`;
  });
}
```

### Card Component Pattern

```typescript
// casino-f/src/app/shared/ui/ui-card.component.ts
export type CardVariant = 'default' | 'elevated' | 'outlined' | 'flat';
export type CardPadding = 'none' | 'sm' | 'md' | 'lg';

@Component({
  selector: 'ui-card',
  template: `
    <div [ngClass]="cardClasses()">
      <div *ngIf="title" class="px-4 py-3 border-b border-slate-200">
        <h3 class="text-sm font-semibold text-slate-900">{{ title }}</h3>
      </div>
      <div [ngClass]="contentClasses()">
        <ng-content></ng-content>
      </div>
    </div>
  `
})
export class UiCardComponent {
  variant = input<CardVariant>('default');
  padding = input<CardPadding>('md');

  cardClasses = computed(() => ({
    'bg-white rounded-lg': true,
    'border border-slate-200 shadow-sm': this.variant() === 'default',
    'shadow-md': this.variant() === 'elevated',
    'border border-slate-300': this.variant() === 'outlined'
  }));
}
```

## Form Components

### Form Field Wrapper

```typescript
// Provides consistent label, required indicator, and error display
<ui-form-field label="Email Address" [required]="true" [error]="emailError">
  <ui-input formControlName="email" type="email" placeholder="user@example.com"></ui-input>
</ui-form-field>
```

### Input Base Styles

```scss
// casino-f/src/styles.scss
@layer components {
  .ui-input-base {
    @apply block w-full rounded-lg border border-slate-300 bg-white px-3 py-2;
    @apply text-sm text-slate-900 shadow-sm placeholder:text-slate-400;
    @apply focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-200;
    @apply disabled:cursor-not-allowed disabled:bg-slate-100 disabled:text-slate-500;
  }
}
```

### WARNING: Inline Styles on Components

**The Problem:**

```typescript
// BAD - Inline styles bypass the design system
@Component({
  template: `
    <button style="background: blue; padding: 10px;">Save</button>
  `
})
```

**Why This Breaks:**
1. Inconsistency - Doesn't match other buttons
2. Unmaintainable - Can't update globally
3. No states - Missing hover, focus, disabled

**The Fix:**

```typescript
// GOOD - Use the component system
@Component({
  template: `
    <ui-button variant="primary" size="md">Save</ui-button>
  `
})
```

## Customer Frontend Components

### CVA Button Pattern

```typescript
// casino-customer-f/src/app/shared/ui/button.component.ts
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        casino: "bg-gradient-to-r from-[#3aa660] to-[#52ea88] text-white hover:from-[#2d8a4d] hover:to-[#3fc970]",
        casinoPurple: "bg-gradient-to-r from-[#8b5cf6] to-[#a855f7] text-white",
        outline: "border border-input bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground"
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3",
        lg: "h-10 rounded-md px-6",
        icon: "h-9 w-9"
      }
    },
    defaultVariants: {
      variant: "default",
      size: "default"
    }
  }
);
```

### WARNING: Creating New Variants Instead of Using Existing

**The Problem:**

```typescript
// BAD - Custom one-off button instead of using existing variant
<button class="bg-green-500 text-white px-4 py-2 rounded">Deposit</button>
```

**Why This Breaks:**
1. Inconsistent hover/focus states
2. Doesn't follow brand gradient
3. Missing accessibility attributes

**The Fix:**

```typescript
// GOOD - Use the casino variant
<button [class]="buttonVariants({ variant: 'casino', size: 'default' })">
  Deposit
</button>
```

## Icon System

### Heroicons via ui-icon

```typescript
// Maps 280+ Material Icons to Heroicons
<ui-icon name="add" size="md"></ui-icon>      <!-- Renders plus icon -->
<ui-icon name="delete" size="sm"></ui-icon>   <!-- Renders trash icon -->
<ui-icon name="edit" size="lg"></ui-icon>     <!-- Renders pencil icon -->
```

Size mapping:
```typescript
const sizeClass = {
  xs: 'h-3 w-3',
  sm: 'h-4 w-4',
  md: 'h-5 w-5',
  lg: 'h-6 w-6',
  xl: 'h-8 w-8'
};
```