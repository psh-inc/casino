---
name: playwright
description: |
  Playwright E2E testing for customer frontend
  Use when: Writing E2E tests for Angular customer frontend, testing authentication flows, testing game listings, testing profile/KYC workflows
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Playwright Skill

Playwright E2E testing for the Angular 17 customer frontend (`casino-customer-f/`). Tests cover authentication, game browsing, wallet operations, KYC verification, and sports betting flows. All tests run headless by default with full browser automation support.

## Quick Start

### Running Tests

```bash
cd casino-customer-f

# Run all E2E tests
npm run e2e

# Interactive UI mode for debugging
npm run e2e:ui

# Run specific test file
npx playwright test tests/auth.spec.ts

# Run with headed browser
npx playwright test --headed
```

### Basic Test Structure

```typescript
// tests/games.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Game Lobby', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/games');
  });

  test('should display game categories', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Slots' })).toBeVisible();
    await expect(page.getByTestId('game-grid')).toHaveCount(1);
  });
});
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Page Object Model | Encapsulate page interactions | `LoginPage.login(user)` |
| Test Fixtures | Share setup across tests | `test.use({ storageState })` |
| Locators | Prefer accessible selectors | `getByRole('button')` |
| Assertions | Use web-first assertions | `await expect(el).toBeVisible()` |
| Snapshots | Visual regression testing | `expect(page).toHaveScreenshot()` |

## Common Patterns

### Authentication Flow Test

**When:** Testing login, registration, or protected routes

```typescript
test('user can login and access wallet', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('test@example.com');
  await page.getByLabel('Password').fill('SecurePass123');
  await page.getByRole('button', { name: 'Sign In' }).click();
  
  await expect(page).toHaveURL('/dashboard');
  await page.getByRole('link', { name: 'Wallet' }).click();
  await expect(page.getByTestId('balance-display')).toBeVisible();
});
```

### Form Validation Testing

**When:** Testing bonus claims, KYC forms, deposit forms

```typescript
test('shows validation errors on invalid deposit', async ({ page }) => {
  await page.goto('/wallet/deposit');
  await page.getByLabel('Amount').fill('-50');
  await page.getByRole('button', { name: 'Deposit' }).click();
  
  await expect(page.getByText('Amount must be positive')).toBeVisible();
});
```

### Waiting for API Responses

**When:** Testing actions that trigger backend calls

```typescript
test('game session starts after API response', async ({ page }) => {
  await page.goto('/games');
  
  const responsePromise = page.waitForResponse('**/api/v1/games/*/session');
  await page.getByTestId('game-card-starburst').click();
  const response = await responsePromise;
  
  expect(response.status()).toBe(200);
  await expect(page.getByTestId('game-iframe')).toBeVisible();
});
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- **angular** - Frontend framework for customer application
- **typescript** - Language for test files