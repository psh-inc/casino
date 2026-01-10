# Promotions Page Redesign Analysis & Implementation Plan

## 1. Complete Design Analysis

### Visual Hierarchy & Layout

#### Page Structure
- **Background**: `casino-gradient-primary` (dark theme gradient)
- **Container Padding**: 
  - Desktop: `px-4 sm:px-6 lg:px-8 xl:px-12 2xl:px-16`
  - Top padding: `pt-32 md:pt-40` (accounts for header)
  - Bottom padding: `pb-12`

#### Main Sections
1. **How to Claim Bonuses** - Instructional card at top
2. **Promotions Grid** - 3-column responsive grid
3. **Responsible Gaming Notice** - Bottom warning section

### Color Palette
```scss
// Primary Colors
$primary-green: #3aa660;
$accent-green: #52ea88;
$green-gradient: linear-gradient(to right, #3aa660, #52ea88);

// Badge Colors
$orange: #f97316 (orange-500);
$purple: #a855f7 (purple-500);
$amber: #f59e0b (amber-500);
$emerald: #10b981 (emerald-500);
$indigo: #6366f1 (indigo-500);
$rose: #f43f5e (rose-500);
$violet: #8b5cf6 (violet-500);

// Background Colors
$card-bg: #1d2f3f;
$dark-bg: #0a1118;
$input-bg: #232c37;

// Text Colors
$text-primary: white;
$text-secondary: rgba(255, 255, 255, 0.9);
$text-muted: rgba(255, 255, 255, 0.6);
$text-subtle: rgba(255, 255, 255, 0.5);

// Border Colors
$border-default: rgba(255, 255, 255, 0.1);
$border-hover: rgba(58, 166, 96, 0.4);
$border-focus: #52ea88;
```

### Typography
```scss
// Font Family
font-family: 'Inter', system-ui, -apple-system, sans-serif;

// Font Sizes
$title-xl: 1.5rem (24px);     // Section titles
$title-lg: 1.25rem (20px);     // Card titles
$title-md: 1.125rem (18px);    // Subtitle
$text-lg: 1rem (16px);         // Large text
$text-base: 0.875rem (14px);   // Body text
$text-sm: 0.75rem (12px);      // Small text
$text-xs: 0.625rem (10px);     // Tiny text

// Font Weights
$font-bold: 700;
$font-semibold: 600;
$font-medium: 500;
$font-normal: 400;
```

### Spacing System
```scss
// Padding/Margin Scale
$space-1: 0.25rem (4px);
$space-2: 0.5rem (8px);
$space-3: 0.75rem (12px);
$space-4: 1rem (16px);
$space-5: 1.25rem (20px);
$space-6: 1.5rem (24px);
$space-8: 2rem (32px);
$space-12: 3rem (48px);

// Component Spacing
$card-padding: 24px;
$card-gap: 32px;
$grid-gap: 32px;
$section-margin: 30px;
```

## 2. Component Structure

### A. How to Claim Bonuses Section
```typescript
interface ClaimStep {
  icon: Component;
  iconBgGradient: string;
  title: string;
  description: string;
}

const steps = [
  {
    icon: UserPlus,
    iconBgGradient: "from-orange-500 to-red-500",
    title: "1. Sign Up",
    description: "Create your BetPortal account in just a few minutes"
  },
  {
    icon: CreditCard,
    iconBgGradient: "from-[#3aa660] to-[#52ea88]",
    title: "2. Deposit",
    description: "Make your qualifying deposit using any payment method"
  },
  {
    icon: Gift,
    iconBgGradient: "from-purple-500 to-purple-600",
    title: "3. Claim",
    description: "Enter promo code or opt-in to activate your bonus"
  },
  {
    icon: Star,
    iconBgGradient: "from-blue-500 to-blue-600",
    title: "4. Play",
    description: "Enjoy your bonus and start playing your favorite games"
  }
];
```

### B. Promotion Card Structure
```typescript
interface Promotion {
  id: number;
  title: string;
  subtitle: string;
  description: string;
  image: string;
  badge: string;
  badgeColor: string;
  expires: string;
  minDeposit: string;
  wagering: string;
  promoCode: string;
  highlights: string[];
  terms: string;
}
```

### C. Card Components

#### 1. Promotion Image Section
- Height: `h-48` (192px)
- Overlay gradient: `from-black/60 to-transparent`
- Image hover effect: `scale-110 transition-transform duration-500`
- Contains: Countdown timer, badge, title, subtitle

#### 2. Countdown Timer
- Position: Top left (`top-3 left-3`)
- Background: `bg-black/80 backdrop-blur-sm`
- Border: `border-orange-400/30`
- Icon: Clock icon with `text-orange-400`
- Text: White, `text-xs font-bold`

#### 3. Badge
- Position: Top right (`top-4 right-4`)
- Dynamic colors based on promotion type
- Font: `text-white font-bold`
- Padding: `px-3 py-1`

#### 4. Card Body
- Padding: `CardHeader pb-4`, `CardContent space-y-4`
- Description: `line-clamp-2` (2 lines max)
- Action buttons: Deposit/Sign Up + Terms button

#### 5. Terms Modal
- Max width: `max-w-2xl`
- Background: `bg-white dark:bg-[#1d2f3f]`
- Contains: Key details grid, highlights list, full terms

## 3. Animations & Interactions

### Motion Animations (Framer Motion)
```typescript
// Card entrance animation
initial={{ opacity: 0, y: 20 }}
animate={{ opacity: 1, y: 0 }}
transition={{ duration: 0.6, delay: index * 0.2 }}

// Hover effects
hover:border-[#3aa660]/40
hover:transform hover:scale-105
transition-all duration-300
```

### Interactive Elements
1. **Card Hover**: Scale 105%, border color change
2. **Image Hover**: Scale 110% with 500ms transition
3. **Button Hover**: Gradient shift, shadow enhancement
4. **Modal Trigger**: Dialog opens with backdrop blur

### Countdown Timer Logic
```javascript
// Dynamic countdown calculation based on promotion type
- "Every Friday": Next Friday at 00:00
- "Every Weekend": Next Saturday at 00:00
- "Every Monday": Next Monday at 00:00
- "Daily": Tomorrow at 00:00
- "7 Days Left": 7 days from now
- "Monthly": Same day next month
- "No Expiry": Shows "∞"
```

## 4. Responsive Design

### Grid Layout
```scss
// Mobile (default): 1 column
grid-cols-1

// Desktop (lg): 3 columns
lg:grid-cols-3

// Gap: 32px between cards
gap-8
```

### Container Breakpoints
```scss
// Padding responsive scale
px-4        // Mobile: 16px
sm:px-6     // Small: 24px
lg:px-8     // Large: 32px
xl:px-12    // XL: 48px
2xl:px-16   // 2XL: 64px
```

## 5. Data Model for API Integration

```typescript
interface PromotionAPIResponse {
  promotions: Promotion[];
  totalCount: number;
  currentPage: number;
  pageSize: number;
}

interface Promotion {
  id: string | number;
  title: string;
  subtitle: string;
  shortDescription: string;
  fullDescription: string;
  imageUrl: string;
  badgeText: string;
  badgeType: 'popular' | 'weekly' | 'weekend' | 'vip' | 'sports' | 'limited' | 'high_roller' | 'monday';
  expiryType: 'no_expiry' | 'daily' | 'weekly' | 'weekend' | 'monthly' | 'countdown';
  expiryValue?: string; // For countdown type
  requirements: {
    minDeposit: string;
    wageringMultiplier: string;
    promoCode?: string;
  };
  highlights: string[];
  termsAndConditions: string;
  cta: {
    primaryText: string;
    primaryAction: 'deposit' | 'signup' | 'claim';
    secondaryText: string;
  };
  status: 'active' | 'upcoming' | 'expired';
  priority: number; // For sorting
  createdAt: string;
  updatedAt: string;
}
```

## 6. Implementation Plan

### Phase 1: Component Setup
1. Create `promotions` folder structure
2. Set up base components:
   - `PromotionsPage.component.ts`
   - `PromotionCard.component.ts`
   - `ClaimSteps.component.ts`
   - `ResponsibleGaming.component.ts`

### Phase 2: Styling Implementation
1. Create SCSS modules following design specs
2. Implement dark theme variables
3. Add gradient utilities
4. Set up animation classes

### Phase 3: Service & API Integration
1. Create `PromotionService`
2. Implement API endpoints
3. Add state management (RxJS)
4. Handle loading/error states

### Phase 4: Interactive Features
1. Implement countdown timer logic
2. Add modal/dialog functionality
3. Create hover effects
4. Add entrance animations

### Phase 5: Testing & Optimization
1. Responsive testing
2. Performance optimization
3. Accessibility improvements
4. Cross-browser testing

## 7. Component File Structure

```
casino-customer-f/
└── src/
    └── app/
        └── features/
            └── promotions/
                ├── promotions-page/
                │   ├── promotions-page.component.ts
                │   ├── promotions-page.component.html
                │   └── promotions-page.component.scss
                ├── components/
                │   ├── promotion-card/
                │   │   ├── promotion-card.component.ts
                │   │   ├── promotion-card.component.html
                │   │   └── promotion-card.component.scss
                │   ├── claim-steps/
                │   │   ├── claim-steps.component.ts
                │   │   ├── claim-steps.component.html
                │   │   └── claim-steps.component.scss
                │   ├── countdown-timer/
                │   │   ├── countdown-timer.component.ts
                │   │   ├── countdown-timer.component.html
                │   │   └── countdown-timer.component.scss
                │   └── promotion-modal/
                │       ├── promotion-modal.component.ts
                │       ├── promotion-modal.component.html
                │       └── promotion-modal.component.scss
                ├── services/
                │   └── promotion.service.ts
                └── models/
                    └── promotion.model.ts
```

## 8. Key Features to Implement

### Must-Have Features
- [x] Responsive 3-column grid layout
- [x] Dark theme with green accents
- [x] Promotion cards with images
- [x] Countdown timers
- [x] Badge system
- [x] Terms modal
- [x] How to claim section
- [x] Responsible gaming notice

### Interactive Features
- [x] Live countdown updates (every second)
- [x] Hover animations
- [x] Modal dialogs for terms
- [x] Conditional CTAs (logged in/out)
- [x] Entrance animations

### Data Features
- [ ] API integration
- [ ] Loading states
- [ ] Error handling
- [ ] Pagination (if needed)
- [ ] Filtering/sorting

## 9. CSS Classes Mapping

### From React (Tailwind) to Angular (Custom SCSS)

```scss
// React Tailwind -> Angular SCSS
.casino-gradient-primary -> .promotions-bg
.casino-card -> .promotion-card
.casino-card-border -> .card-border
.casino-text-primary -> .text-primary
.casino-text-secondary -> .text-secondary
.casino-text-muted -> .text-muted
.bg-gradient-to-r -> .gradient-horizontal
.from-[#3aa660] to-[#52ea88] -> .gradient-green
.hover:scale-105 -> .hover-scale
.transition-all duration-300 -> .smooth-transition
```

## 10. Notes for Implementation

1. **Countdown Timer**: Implement as a separate component with Input for expiry type
2. **Badge Colors**: Create an enum or map for badge type -> color class
3. **Animations**: Use Angular Animations API or CSS animations
4. **Modal**: Use Angular Material Dialog or custom implementation
5. **Grid**: Use CSS Grid with proper breakpoints
6. **Images**: Implement lazy loading for performance
7. **Accessibility**: Add proper ARIA labels and keyboard navigation

## Ready for Implementation
All design specifications have been extracted and documented. The implementation can proceed with the API structure defined above. When the API is ready, we can integrate it seamlessly with this design.