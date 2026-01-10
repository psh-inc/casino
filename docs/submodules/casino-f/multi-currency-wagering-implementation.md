# Multi-Currency Wagering Limits Implementation

## Overview
This document describes the implementation of multi-currency support for wagering limits in the bonus system frontend.

## Changes Implemented

### 1. Interface Updates (`bonus.service.ts`)

#### BonusRequest Interface
Added multi-currency fields:
```typescript
// Multi-currency wagering limits
maxBetAmounts?: { [currency: string]: number };
minAmountsToTerminate?: { [currency: string]: number };
maxWinAmounts?: { [currency: string]: number };

// Deprecated single-currency fields - kept for backward compatibility
maxBetAmount?: number; // @deprecated Use maxBetAmounts instead
minAmountToTerminate?: number; // @deprecated Use minAmountsToTerminate instead
maxWinAmountEur?: number; // @deprecated Use maxWinAmounts instead
```

### 2. Service Methods Updates

#### convertToBackendFormat Method
Updated to map multi-currency fields to backend format:
```typescript
// Wagering restrictions - use multi-currency maps if available, fallback to single values
maxBetAmounts: bonus.maxBetAmounts || (bonus.maxBetAmount ? { EUR: bonus.maxBetAmount } : undefined),
minAmountsToTerminate: bonus.minAmountsToTerminate || (bonus.minAmountToTerminate ? { EUR: bonus.minAmountToTerminate } : undefined),
maxWinAmounts: bonus.maxWinAmounts || (bonus.maxWinAmountEur ? { EUR: bonus.maxWinAmountEur } : undefined),
```

#### mapBackendBonusToFrontend Method
Updated to map backend response fields:
```typescript
// Multi-currency wagering limits from backend
maxBetAmounts: backendBonus.maxBetAmounts || {},
minAmountsToTerminate: backendBonus.minAmountsToTerminate || {},
maxWinAmounts: backendBonus.maxWinAmounts || {},

// Legacy single-currency fields for backward compatibility
maxBetAmount: backendBonus.maxBetAmount,
minAmountToTerminate: backendBonus.minAmountToTerminate,
maxWinAmountEur: backendBonus.maxWinAmountEur,
```

### 3. Component Updates (`bonus-form.component.ts`)

#### Dynamic Form Control Management
Enhanced `updatePerCurrencyControls` method to manage wagering form controls:
```typescript
// Add/remove wagering limit controls in wageringForm
currencies.forEach(currency => {
  const maxBetKey = `maxBet_${currency}`;
  const minTerminateKey = `minTerminate_${currency}`;
  const maxWinKey = `maxWin_${currency}`;
  
  // Add controls if they don't exist
  if (!this.wageringForm.contains(maxBetKey)) {
    this.wageringForm.addControl(maxBetKey, this.fb.control(null));
  }
  // ... similar for other controls
});
```

#### Building Request Data
Added `buildWageringLimits` helper method:
```typescript
private buildWageringLimits(wageringFormValue: any, fieldPrefix: string): { [currency: string]: number } | undefined {
  const limits: { [currency: string]: number } = {};
  const currencies = this.generalForm.get('eligibleCurrencies')?.value || ['EUR'];
  let hasAnyValue = false;
  
  currencies.forEach((currency: string) => {
    const key = `${fieldPrefix}_${currency}`;
    const value = wageringFormValue[key];
    
    if (value !== null && value !== undefined && value !== '') {
      limits[currency] = Number(value);
      hasAnyValue = true;
    }
  });
  
  return hasAnyValue ? limits : undefined;
}
```

Updated `buildBonusRequest` to use the new multi-currency fields:
```typescript
// Multi-currency wagering limits
maxBetAmounts: this.buildWageringLimits(wagering, 'maxBet'),
minAmountsToTerminate: this.buildWageringLimits(wagering, 'minTerminate'),
maxWinAmounts: this.buildWageringLimits(wagering, 'maxWin'),
```

#### Loading Bonus Data
Enhanced `populateFormsFromBonus` to handle multi-currency data:
```typescript
// Populate multi-currency wagering limits
const currencies = bonus.eligibleCurrencies || ['EUR'];
currencies.forEach(currency => {
  // Max bet amounts
  if (bonus.maxBetAmounts && bonus.maxBetAmounts[currency] !== undefined) {
    this.wageringForm.patchValue({ [`maxBet_${currency}`]: bonus.maxBetAmounts[currency] });
  } else if (bonus.maxBetAmount && currency === 'EUR') {
    // Fallback to legacy single value for EUR
    this.wageringForm.patchValue({ [`maxBet_EUR`]: bonus.maxBetAmount });
  }
  // Similar for other fields...
});
```

#### Currency Symbol Helper
Added method to display currency symbols:
```typescript
getCurrencySymbol(currency: string): string {
  const symbols: { [key: string]: string } = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'CAD': 'C$',
    // ... more currencies
  };
  return symbols[currency] || currency + ' ';
}
```

### 4. Template Updates (`bonus-form.component.html`)

#### Wagering Requirements Section
Replaced single currency fields with dynamic per-currency fields:
```html
<!-- Per-Currency Wagering Limits -->
<div *ngIf="generalForm.get('eligibleCurrencies')?.value?.length" class="currency-limits-container">
  <div *ngFor="let currency of generalForm.get('eligibleCurrencies')?.value" class="currency-section">
    <h4 class="currency-title">{{ currency }} Limits</h4>
    
    <div class="form-row">
      <div class="form-field">
        <label class="field-label">Max Bet Amount</label>
        <div class="input-group">
          <span class="input-prefix">{{ getCurrencySymbol(currency) }}</span>
          <input type="number" 
                 class="field-input" 
                 [formControlName]="'maxBet_' + currency"
                 placeholder="e.g. 5"
                 min="0"
                 step="0.01">
        </div>
      </div>
      <!-- Similar for other fields -->
    </div>
  </div>
</div>
```

#### Review Section
Updated to display per-currency limits:
```html
<!-- Per-Currency Wagering Limits -->
<div *ngFor="let currency of generalForm.get('eligibleCurrencies')?.value">
  <div class="review-item" *ngIf="wageringForm.get('maxBet_' + currency)?.value">
    <span class="review-label">Max Bet ({{ currency }}):</span>
    <span class="review-value">{{ getCurrencySymbol(currency) }}{{ wageringForm.get('maxBet_' + currency)?.value }}</span>
  </div>
  <!-- Similar for other fields -->
</div>
```

### 5. Styling Updates (`bonus-form.component.css`)

Added styles for currency sections:
```css
.currency-limits-container {
  margin-top: 20px;
}

.currency-section {
  background: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.currency-title {
  font-size: 16px;
  font-weight: 600;
  color: #424242;
  margin: 0 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #e0e0e0;
}

.info-message {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f0f4f8;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  color: #656d76;
  margin-top: 20px;
}
```

## Backward Compatibility

The implementation maintains full backward compatibility:

1. **Old Fields Preserved**: The deprecated single-currency fields (`maxBetAmount`, `minAmountToTerminate`, `maxWinAmountEur`) are kept in the interfaces
2. **Automatic Migration**: When loading bonuses with old format, the values are automatically mapped to EUR in the multi-currency format
3. **Fallback Logic**: The service methods check for multi-currency data first, then fall back to single-currency fields if not present
4. **Seamless Upgrade**: Existing bonuses continue to work without modification

## Usage

### Creating a New Bonus
1. Select eligible currencies in the General Setup step
2. Navigate to the Wagering Requirements step
3. Configure limits for each selected currency in the dedicated currency sections
4. The form automatically creates/removes currency fields based on selected currencies

### Editing an Existing Bonus
1. The form automatically detects if the bonus uses old or new format
2. Old single-currency values are displayed in the EUR section
3. User can add limits for additional currencies as needed

## Testing

### Manual Testing Steps
1. Create a new bonus with multiple currencies (EUR, USD, GBP)
2. Set different wagering limits for each currency
3. Save the bonus and verify the data is sent correctly to the backend
4. Load an existing bonus and verify multi-currency limits are displayed
5. Test backward compatibility by loading a bonus with old single-currency format

### Validation Points
- Currency fields are dynamically added/removed when currencies are selected/deselected
- Currency symbols are displayed correctly
- Values are properly formatted and sent to the backend
- Review section shows all configured limits
- Form validation works correctly for numeric inputs

## Future Enhancements

1. **Bulk Currency Operations**: Add ability to apply the same limit to all currencies at once
2. **Currency Conversion**: Show approximate values in other currencies for reference
3. **Templates**: Save common limit configurations as templates
4. **Import/Export**: Support CSV import/export for multi-currency limits