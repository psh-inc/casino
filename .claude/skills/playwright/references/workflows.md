# Playwright Workflows

## Test Organization

Structure tests by user journey for the customer frontend:

```
casino-customer-f/
├── tests/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   ├── registration.spec.ts
│   │   └── password-reset.spec.ts
│   ├── games/
│   │   ├── lobby.spec.ts
│   │   ├── game-session.spec.ts
│   │   └── search-filters.spec.ts
│   ├── wallet/
│   │   ├── deposit.spec.ts
│   │   └── withdrawal.spec.ts
│   ├── kyc/
│   │   └── document-upload.spec.ts
│   ├── pages/              # Page Object Models
│   │   ├── login.page.ts
│   │   ├── games.page.ts
│   │   └── wallet.page.ts
│   └── fixtures/
│       └── auth.fixture.ts
├── playwright.config.ts
└── package.json
```

---

## Authentication Fixture

Reuse authenticated state across tests:

```typescript
// tests/fixtures/auth.fixture.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/login.page';

type AuthFixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(
      process.env.TEST_USER_EMAIL!,
      process.env.TEST_USER_PASSWORD!
    );
    await page.waitForURL('/dashboard');
    await use(page);
  },
});
```

### Using the Fixture

```typescript
// tests/wallet/deposit.spec.ts
import { test } from '../fixtures/auth.fixture';
import { expect } from '@playwright/test';

test('authenticated user can access deposit page', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/wallet/deposit');
  await expect(authenticatedPage.getByRole('heading', { name: 'Deposit' })).toBeVisible();
});
```

---

## CI/CD Integration

### Playwright Configuration for CI

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI ? 'github' : 'html',
  
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:4201',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  webServer: process.env.CI ? undefined : {
    command: 'ng serve',
    url: 'http://localhost:4201',
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## Debugging Workflow

### Interactive Debugging

```bash
# Run with UI for step-by-step debugging
npm run e2e:ui

# Run specific test in debug mode
npx playwright test tests/auth/login.spec.ts --debug

# Generate trace for failed test analysis
npx playwright test --trace on
```

### Trace Viewer

```bash
# View trace file after failure
npx playwright show-trace test-results/auth-login-chromium/trace.zip
```

---

## WARNING: Testing Implementation Details

**The Problem:**

```typescript
// BAD - Testing Angular internals
test('component state updates', async ({ page }) => {
  await page.goto('/games');
  // Checking internal component properties
  const componentState = await page.evaluate(() => {
    return (window as any).ng.getComponent(
      document.querySelector('app-game-list')
    ).games.length;
  });
  expect(componentState).toBe(10);
});
```

**Why This Breaks:**
1. Tightly coupled to Angular implementation
2. Breaks when component internals change
3. Not testing actual user experience

**The Fix:**

```typescript
// GOOD - Test user-visible behavior
test('game list displays games', async ({ page }) => {
  await page.goto('/games');
  await expect(page.getByTestId('game-card')).toHaveCount(10);
});
```

---

## Multi-Language Testing

Test localized content for i18n support:

```typescript
// tests/i18n/locale-switching.spec.ts
import { test, expect } from '@playwright/test';

const locales = ['en', 'de', 'fr', 'es'];

for (const locale of locales) {
  test(`displays correct content for ${locale}`, async ({ page }) => {
    await page.goto(`/${locale}/games`);
    
    // Verify locale-specific content renders
    await expect(page.locator('html')).toHaveAttribute('lang', locale);
    await expect(page.getByRole('navigation')).toBeVisible();
  });
}
```

---

## Visual Regression Testing

Catch unintended UI changes:

```typescript
test('game lobby matches snapshot', async ({ page }) => {
  await page.goto('/games');
  await page.waitForLoadState('networkidle');
  
  // Full page screenshot
  await expect(page).toHaveScreenshot('game-lobby.png', {
    maxDiffPixels: 100,
  });
});

test('deposit form matches snapshot', async ({ page }) => {
  await page.goto('/wallet/deposit');
  
  // Component screenshot
  await expect(page.getByTestId('deposit-form')).toHaveScreenshot('deposit-form.png');
});
```

Update snapshots when intentional changes occur:

```bash
npx playwright test --update-snapshots
```