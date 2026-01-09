# Playwright Patterns

## Page Object Model

Encapsulate page interactions in reusable classes. This is critical for maintainability as the customer frontend evolves.

### Login Page Object

```typescript
// tests/pages/login.page.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign In' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}
```

### WARNING: Hardcoded Selectors

**The Problem:**

```typescript
// BAD - Brittle CSS selectors
await page.click('.btn-primary.login-submit');
await page.locator('#form-email-input-123').fill('test@example.com');
```

**Why This Breaks:**
1. CSS classes change during UI refactoring - tests break silently
2. Generated IDs change per build or session
3. No semantic meaning - can't understand what the test is doing

**The Fix:**

```typescript
// GOOD - Accessible, semantic selectors
await page.getByRole('button', { name: 'Sign In' }).click();
await page.getByLabel('Email').fill('test@example.com');
await page.getByTestId('login-form').getByRole('textbox').first().fill('test');
```

**When You Might Be Tempted:**
Copy-pasting selectors from browser DevTools seems faster, but leads to test rot.

---

## Locator Strategy Priority

Use this hierarchy for element selection:

| Priority | Method | When to Use |
|----------|--------|-------------|
| 1 | `getByRole()` | Buttons, links, headings, inputs |
| 2 | `getByLabel()` | Form inputs with labels |
| 3 | `getByText()` | Unique text content |
| 4 | `getByTestId()` | Dynamic or complex elements |
| 5 | CSS selectors | Last resort only |

### Role-Based Selectors

```typescript
// Preferred for Angular Material components
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('link', { name: 'Games' }).click();
await page.getByRole('heading', { level: 1 }).toHaveText('Welcome');
await page.getByRole('checkbox', { name: 'Remember me' }).check();
```

---

## Waiting Patterns

### WARNING: Arbitrary Timeouts

**The Problem:**

```typescript
// BAD - Arbitrary sleep
await page.goto('/games');
await page.waitForTimeout(3000);
await page.click('[data-testid="game-card"]');
```

**Why This Breaks:**
1. Tests are slow (always wait full duration)
2. Flaky on slow CI - 3s might not be enough
3. No relationship to actual page state

**The Fix:**

```typescript
// GOOD - Wait for specific conditions
await page.goto('/games');
await page.waitForLoadState('networkidle');
await page.getByTestId('game-card').first().click();

// Or wait for specific element
await page.goto('/games');
await expect(page.getByTestId('game-grid')).toBeVisible();
await page.getByTestId('game-card').first().click();
```

---

## API Mocking

Mock backend responses for isolated frontend testing:

```typescript
test('handles empty game list gracefully', async ({ page }) => {
  await page.route('**/api/v1/games*', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ content: [], totalElements: 0 }),
    });
  });

  await page.goto('/games');
  await expect(page.getByText('No games available')).toBeVisible();
});

test('handles API errors', async ({ page }) => {
  await page.route('**/api/v1/wallet/balance', async (route) => {
    await route.fulfill({ status: 500 });
  });

  await page.goto('/wallet');
  await expect(page.getByText('Failed to load balance')).toBeVisible();
});
```

---

## Test Data Management

### WARNING: Shared Mutable Test Data

**The Problem:**

```typescript
// BAD - Tests depend on shared state
const testUser = { email: 'test@casino.com', balance: 100 };

test('user deposits money', async ({ page }) => {
  await depositMoney(page, testUser, 50);
  // testUser.balance is now 150 in DB
});

test('user has correct balance', async ({ page }) => {
  // FLAKY: Depends on previous test running first
  await expect(page.getByTestId('balance')).toHaveText('150');
});
```

**The Fix:**

```typescript
// GOOD - Isolated test data per test
test('user deposits money', async ({ page, request }) => {
  // Create fresh user via API
  const user = await request.post('/api/test/create-user', {
    data: { email: `test-${Date.now()}@casino.com` }
  });
  
  await loginAs(page, user);
  await depositMoney(page, 50);
  await expect(page.getByTestId('balance')).toContainText('50');
});
```