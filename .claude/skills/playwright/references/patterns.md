# Playwright Testing Patterns

Patterns specific to the casino customer frontend E2E testing setup.

## Element Selection Patterns

### DO: Use Role-Based Selectors

```typescript
// GOOD - Accessible, resilient to implementation changes
await page.getByRole('button', { name: 'Login' }).first().click();
await page.getByRole('button', { name: 'Sign In', exact: true }).click();
```

### DON'T: Use Fragile CSS Selectors

```typescript
// BAD - Breaks when CSS classes change
await page.click('button.btn-primary.login-btn');
await page.click('#login-button');
```

**Why:** Role-based selectors match accessibility semantics, making tests resilient to CSS refactoring while ensuring your app is accessible.

## Form Control Selection

### Angular FormControl Pattern

```typescript
// CORRECT - Matches Angular reactive form structure
await page.locator('input[formControlName="username"]').fill('testuser');
await page.locator('input[formControlName="password"]').fill('password');
await page.locator('input[formControlName="termsAccepted"]').check();
```

### Dynamic Form Fields (Registration)

```typescript
// For dynamically generated form fields with IDs
await page.locator('input#field-1').fill('testuser');      // Username
await page.locator('input#field-2').fill('test@test.com'); // Email
await page.locator('input#field-3').fill('Password123!');  // Password
```

## WARNING: Hardcoded Timeouts

**The Problem:**

```typescript
// BAD - Arbitrary wait causes flaky tests
await page.waitForTimeout(5000);
await page.locator('.games-content').click();
```

**Why This Breaks:**
1. Tests become slow (always waiting max time)
2. Flaky on slower CI environments
3. No connection to actual application state

**The Fix:**

```typescript
// GOOD - Wait for specific conditions
await page.waitForSelector('.games-content', { state: 'visible' });
await page.waitForLoadState('networkidle');
await expect(page.locator('.games-content')).toBeVisible({ timeout: 10000 });
```

**When You Might Be Tempted:** After form submission, API calls, or animations. Instead, wait for the resulting UI state.

## API Mocking Pattern

### Mock Registration Config

```typescript
await page.route('**/public/registration/signup-config', route => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      accountFields: [
        { id: 1, fieldName: 'Username', fieldType: 'TEXT', isRequired: true }
      ],
      termsAndConditions: { requiresAcceptance: true }
    })
  });
});
```

### Mock Username Availability Check

```typescript
await page.route('**/public/registration/check-username**', route => {
  const url = new URL(route.request().url());
  const username = url.searchParams.get('username');
  
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      available: username !== 'taken',
      message: username === 'taken' ? 'Username is already taken' : null
    })
  });
});
```

## WARNING: Missing API Route Mocks

**The Problem:**

```typescript
// BAD - Test depends on backend state
test('should register user', async ({ page }) => {
  await page.goto('/register');
  // Fails if backend is down or returns different data
});
```

**Why This Breaks:**
1. Tests fail when backend is unavailable
2. Inconsistent test data across environments
3. Cannot test error states reliably

**The Fix:**

```typescript
// GOOD - Mock all external dependencies
test('should register user', async ({ page }) => {
  await page.route('**/public/registration/signup-config', route => {
    route.fulfill({ status: 200, body: JSON.stringify(mockConfig) });
  });
  
  await page.route('**/auth/register', route => {
    route.fulfill({ status: 201, body: JSON.stringify({ id: 1 }) });
  });
  
  await page.goto('/register');
});
```

## Mobile Viewport Testing

```typescript
test('should handle mobile responsiveness', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
  
  await page.goto('http://localhost:4201/games');
  await expect(page.locator('.games-page')).toBeVisible();
  
  // Verify mobile-specific elements
  const modalContainer = page.locator('.auth-modal-container');
  const modalBox = await modalContainer.boundingBox();
  const viewport = page.viewportSize();
  
  expect(modalBox?.width).toBe(viewport?.width);
});
```

## Backdrop Click Pattern

```typescript
// Click at specific position to hit backdrop, not modal content
await page.locator('.auth-modal-backdrop').click({ position: { x: 10, y: 10 } });
await expect(page.locator('.auth-modal-backdrop')).not.toBeVisible();
```

## WARNING: Using `page.$` Instead of Locators

**The Problem:**

```typescript
// BAD - Returns null instead of waiting, prone to race conditions
const element = await page.$('.my-element');
if (element) {
  await element.click();
}
```

**Why This Breaks:**
1. No auto-waiting behavior
2. Race conditions with dynamic content
3. Requires manual null checks

**The Fix:**

```typescript
// GOOD - Locators have auto-wait and retry logic
const element = page.locator('.my-element');
if (await element.count() > 0) {
  await element.click();
}

// Or use expect for assertions
await expect(page.locator('.my-element')).toBeVisible();
```