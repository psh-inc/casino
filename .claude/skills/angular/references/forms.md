# Angular Reactive Forms Patterns

## Basic Form Setup

All forms in this codebase use Reactive Forms, never Template-driven forms.

### Standard Form Pattern

```typescript
@Component({
  selector: 'app-currency-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, UiFormFieldComponent]
})
export class CurrencyFormComponent implements OnInit {
  currencyForm!: FormGroup;
  isEditMode = false;
  loading = false;

  constructor(
    private fb: FormBuilder,
    private currencyService: CurrencyService,
    private dialogRef: MatDialogRef<CurrencyFormComponent>,
    @Inject(MAT_DIALOG_DATA) public data: Currency | null
  ) {}

  ngOnInit(): void {
    this.isEditMode = !!this.data?.id;
    this.initializeForm();
  }

  private initializeForm(): void {
    this.currencyForm = this.fb.group({
      code: [
        { value: this.data?.code || '', disabled: this.isEditMode },
        [Validators.required, Validators.minLength(2), Validators.maxLength(10)]
      ],
      name: [this.data?.name || '', [Validators.required, Validators.maxLength(100)]],
      minDeposit: [this.data?.minDeposit || null, [Validators.min(0)]],
      maxDeposit: [this.data?.maxDeposit || null, [Validators.min(0)]],
      isActive: [this.data?.isActive ?? true]
    });

    this.currencyForm.setValidators(this.limitsValidator);
  }

  limitsValidator(group: FormGroup): ValidationErrors | null {
    const min = group.get('minDeposit')?.value;
    const max = group.get('maxDeposit')?.value;
    if (min && max && min > max) {
      return { depositLimits: 'Minimum cannot exceed maximum' };
    }
    return null;
  }

  onSubmit(): void {
    if (this.currencyForm.invalid) {
      this.markAllAsTouched();
      return;
    }

    this.loading = true;
    const formValue = this.currencyForm.getRawValue();  // Includes disabled fields

    const save$ = this.isEditMode
      ? this.currencyService.update(this.data!.id!, formValue)
      : this.currencyService.create(formValue);

    save$.subscribe({
      next: (result) => {
        this.dialogRef.close(result);
      },
      error: (error) => {
        console.error('Save failed:', error);
        this.loading = false;
      }
    });
  }

  private markAllAsTouched(): void {
    Object.keys(this.currencyForm.controls).forEach(key => {
      const control = this.currencyForm.get(key);
      if (control?.invalid) {
        control.markAsTouched();
      }
    });
  }
}
```

---

## WARNING: Using Template-Driven Forms

**The Problem:**

```html
<!-- BAD - Template-driven form -->
<form #myForm="ngForm" (ngSubmit)="onSubmit(myForm.value)">
  <input [(ngModel)]="user.name" name="name" required>
</form>
```

**Why This Breaks:**
1. Logic scattered between template and component
2. Harder to unit test (requires DOM)
3. Complex validation is awkward
4. Dynamic forms are difficult
5. Inconsistent with codebase patterns

**The Fix:**

```typescript
// GOOD - Reactive form
this.form = this.fb.group({
  name: ['', Validators.required]
});
```

```html
<form [formGroup]="form" (ngSubmit)="onSubmit()">
  <input formControlName="name">
</form>
```

---

## WARNING: Not Showing Validation Errors

**The Problem:**

```html
<!-- BAD - No feedback to user -->
<input formControlName="email">
<button type="submit">Save</button>
```

**Why This Breaks:**
1. Users don't know what's wrong
2. Form appears broken
3. Bad UX, support tickets

**The Fix:**

```html
<!-- GOOD - Clear error messages -->
<input formControlName="email" [class.error]="form.get('email')?.invalid && form.get('email')?.touched">
<div *ngIf="form.get('email')?.invalid && form.get('email')?.touched" class="error-message">
  <span *ngIf="form.get('email')?.errors?.['required']">Email is required</span>
  <span *ngIf="form.get('email')?.errors?.['email']">Invalid email format</span>
</div>
```

---

## Cross-Field Validation

```typescript
private initializeForm(): void {
  this.form = this.fb.group({
    password: ['', [Validators.required, Validators.minLength(8)]],
    confirmPassword: ['', Validators.required]
  });

  // Form-level validator
  this.form.setValidators(this.passwordMatchValidator);
}

passwordMatchValidator(form: FormGroup): ValidationErrors | null {
  const password = form.get('password')?.value;
  const confirm = form.get('confirmPassword')?.value;
  
  if (password && confirm && password !== confirm) {
    return { passwordMismatch: true };
  }
  return null;
}
```

```html
<div *ngIf="form.errors?.['passwordMismatch']" class="error-message">
  Passwords do not match
</div>
```

---

## Dynamic Form Controls

```typescript
// BonusFormStateService pattern - rewards array
private initializeRewardsArray(): void {
  this.rewardsForm = this.fb.group({
    rewards: this.fb.array([])
  });
}

get rewardsArray(): FormArray {
  return this.rewardsForm.get('rewards') as FormArray;
}

addReward(type: RewardType): void {
  const rewardGroup = this.fb.group({
    type: [type, Validators.required],
    amount: [null, [Validators.required, Validators.min(0)]],
    currency: ['EUR', Validators.required]
  });

  this.rewardsArray.push(rewardGroup);
}

removeReward(index: number): void {
  this.rewardsArray.removeAt(index);
}
```

```html
<div *ngFor="let reward of rewardsArray.controls; let i = index" [formGroupName]="i">
  <input formControlName="amount" type="number">
  <select formControlName="currency">...</select>
  <button (click)="removeReward(i)">Remove</button>
</div>
```

---

## Form State Service (Wizard Pattern)

```typescript
@Injectable({ providedIn: 'root' })
export class BonusFormStateService {
  private formState = new BehaviorSubject<BonusFormState>(this.getInitialState());

  getFormState(): Observable<BonusFormState> {
    return this.formState.asObservable();
  }

  updateStep(step: string, data: Partial<BonusFormState>): void {
    const current = this.formState.value;
    this.formState.next({ ...current, ...data, lastUpdatedStep: step });
  }

  setCategory(category: BonusCategory): void {
    this.updateStep('general', { category });
  }

  reset(): void {
    this.formState.next(this.getInitialState());
  }

  private getInitialState(): BonusFormState {
    return {
      category: null,
      name: '',
      rewards: [],
      lastUpdatedStep: null
    };
  }
}
```

---

## Async Validation

```typescript
// Check if username is already taken
usernameValidator(control: AbstractControl): Observable<ValidationErrors | null> {
  if (!control.value) return of(null);

  return this.userService.checkUsername(control.value).pipe(
    debounceTime(300),
    map(exists => exists ? { usernameTaken: true } : null),
    catchError(() => of(null))
  );
}

// Usage
this.form = this.fb.group({
  username: ['', [Validators.required], [this.usernameValidator.bind(this)]]
});
```

---

## Quick Reference

| Task | Method |
|------|--------|
| Get form value | `form.value` or `form.getRawValue()` |
| Check validity | `form.valid` / `form.invalid` |
| Mark as touched | `control.markAsTouched()` |
| Reset form | `form.reset()` or `form.reset(initialValues)` |
| Disable field | `control.disable()` |
| Get nested control | `form.get('address.city')` |
| Patch partial values | `form.patchValue({ name: 'New' })` |