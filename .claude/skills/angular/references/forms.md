# Reactive Forms Patterns

This project uses Angular Reactive Forms with FormBuilder.

## Basic Form Setup

```typescript
@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.component.html'
})
export class LoginComponent implements OnInit, OnDestroy {
  private fb = inject(FormBuilder);
  private destroy$ = new Subject<void>();
  
  loginForm!: FormGroup;
  loading = false;
  error: string | null = null;

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      rememberMe: [false]
    });
    
    // Clear error when user types
    this.loginForm.valueChanges.pipe(
      takeUntil(this.destroy$)
    ).subscribe(() => this.error = null);
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.markFormTouched();
      return;
    }
    
    this.loading = true;
    this.authService.login(this.loginForm.value).pipe(
      finalize(() => this.loading = false)
    ).subscribe({
      next: () => this.router.navigate(['/dashboard']),
      error: err => this.error = err.message
    });
  }

  private markFormTouched(): void {
    Object.keys(this.loginForm.controls).forEach(key => {
      this.loginForm.get(key)?.markAsTouched();
    });
  }
  
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

## Template Integration

```html
<form [formGroup]="loginForm" (ngSubmit)="onSubmit()">
  <div class="form-field">
    <input formControlName="username" placeholder="Username" />
    <span *ngIf="loginForm.get('username')?.touched && loginForm.get('username')?.errors?.['required']">
      Username is required
    </span>
  </div>
  
  <div class="form-field">
    <input type="password" formControlName="password" placeholder="Password" />
    <span *ngIf="loginForm.get('password')?.touched && loginForm.get('password')?.errors?.['minlength']">
      Password must be at least 8 characters
    </span>
  </div>
  
  <label>
    <input type="checkbox" formControlName="rememberMe" />
    Remember me
  </label>
  
  <button type="submit" [disabled]="loading">
    {{ loading ? 'Signing in...' : 'Sign In' }}
  </button>
  
  <div *ngIf="error" class="error">{{ error }}</div>
</form>
```

## WARNING: Using ngModel with Reactive Forms

**The Problem:**

```html
<!-- BAD - Mixing template-driven and reactive forms -->
<form [formGroup]="myForm">
  <input formControlName="email" [(ngModel)]="email" />
</form>
```

**Why This Breaks:**
1. Two sources of truth for same value
2. Deprecated in Angular (will be removed)
3. Unpredictable behavior and timing issues

**The Fix:**

```html
<!-- GOOD - Reactive forms only -->
<form [formGroup]="myForm">
  <input formControlName="email" />
</form>
```

## Dynamic Form Fields

```typescript
// From ProfileComponent - dynamic field configuration
interface FieldConfig {
  name: string;
  type: 'TEXT' | 'SELECT' | 'DATE' | 'PHONE' | 'MULTISELECT';
  label: string;
  required: boolean;
  options?: { value: string; label: string }[];
}

export class ProfileComponent {
  dynamicForm!: FormGroup;
  fieldConfigs: FieldConfig[] = [];

  buildDynamicForm(configs: FieldConfig[]): void {
    const formGroup: { [key: string]: FormControl } = {};
    
    configs.forEach(config => {
      const validators = config.required ? [Validators.required] : [];
      formGroup[config.name] = new FormControl('', validators);
    });
    
    this.dynamicForm = this.fb.group(formGroup);
  }
}
```

## WARNING: Not Unsubscribing from valueChanges

**The Problem:**

```typescript
// BAD - Memory leak from form subscription
ngOnInit(): void {
  this.form.valueChanges.subscribe(value => {
    this.autoSave(value);
  });
}
```

**The Fix:**

```typescript
// GOOD - Proper cleanup
ngOnInit(): void {
  this.form.valueChanges.pipe(
    debounceTime(500),
    takeUntil(this.destroy$)
  ).subscribe(value => this.autoSave(value));
}
```

## Form Arrays Pattern

```typescript
// Deposit limits form with multiple entries
limitsForm = this.fb.group({
  limits: this.fb.array([])
});

get limitsArray(): FormArray {
  return this.limitsForm.get('limits') as FormArray;
}

addLimit(): void {
  this.limitsArray.push(this.fb.group({
    period: ['DAILY', Validators.required],
    amount: ['', [Validators.required, Validators.min(0)]]
  }));
}

removeLimit(index: number): void {
  this.limitsArray.removeAt(index);
}
```