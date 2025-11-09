# Example: React Component Testing - Payment Form

Complete test suite generation for React component with TanStack Query - from zero tests to 100% coverage.

## Context

**Component**: Payment form for e-commerce checkout
**Initial State**: 0 tests, 0% coverage
**Problem**: Shipping to production without tests (risky!)
**Technologies**: React 19, TypeScript, Vite, Vitest, Testing Library, TanStack Query

**Component Features**:
- Form validation (credit card, expiry, CVV)
- TanStack Query mutation for payment processing
- Loading states and error handling
- Accessibility (ARIA labels, keyboard nav)
- Success/error toast notifications

## Initial Code (Untested)

**File**: `src/components/PaymentForm.tsx`

```typescript
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';

interface PaymentFormProps {
  orderId: string;
  amount: number;
  onSuccess: () => void;
}

export function PaymentForm({ orderId, amount, onSuccess }: PaymentFormProps) {
  const [cardNumber, setCardNumber] = useState('');
  const [expiry, setExpiry] = useState('');
  const [cvv, setCvv] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});

  const paymentMutation = useMutation({
    mutationFn: async (paymentData: any) => {
      const response = await fetch('/api/payments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(paymentData),
      });

      if (!response.ok) {
        throw new Error('Payment failed');
      }

      return response.json();
    },
    onSuccess: () => {
      toast.success('Payment successful!');
      onSuccess();
    },
    onError: (error: Error) => {
      toast.error(error.message);
    },
  });

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    // Card number validation (simple version)
    if (!cardNumber || cardNumber.length < 16) {
      newErrors.cardNumber = 'Invalid card number';
    }

    // Expiry validation (MM/YY format)
    if (!expiry.match(/^\d{2}\/\d{2}$/)) {
      newErrors.expiry = 'Invalid expiry (MM/YY)';
    }

    // CVV validation
    if (!cvv || cvv.length < 3) {
      newErrors.cvv = 'Invalid CVV';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      paymentMutation.mutate({
        orderId,
        amount,
        cardNumber,
        expiry,
        cvv,
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} aria-label="Payment form">
      <div>
        <label htmlFor="cardNumber">Card Number</label>
        <input
          id="cardNumber"
          type="text"
          value={cardNumber}
          onChange={(e) => setCardNumber(e.target.value)}
          maxLength={16}
          aria-invalid={!!errors.cardNumber}
          aria-describedby={errors.cardNumber ? 'cardNumber-error' : undefined}
        />
        {errors.cardNumber && (
          <span id="cardNumber-error" role="alert">
            {errors.cardNumber}
          </span>
        )}
      </div>

      <div>
        <label htmlFor="expiry">Expiry (MM/YY)</label>
        <input
          id="expiry"
          type="text"
          value={expiry}
          onChange={(e) => setExpiry(e.target.value)}
          placeholder="MM/YY"
          maxLength={5}
          aria-invalid={!!errors.expiry}
        />
        {errors.expiry && <span role="alert">{errors.expiry}</span>}
      </div>

      <div>
        <label htmlFor="cvv">CVV</label>
        <input
          id="cvv"
          type="text"
          value={cvv}
          onChange={(e) => setCvv(e.target.value)}
          maxLength={4}
          aria-invalid={!!errors.cvv}
        />
        {errors.cvv && <span role="alert">{errors.cvv}</span>}
      </div>

      <button type="submit" disabled={paymentMutation.isPending}>
        {paymentMutation.isPending ? 'Processing...' : `Pay $${amount}`}
      </button>
    </form>
  );
}
```

## Test Generation Process

### Step 1: Analyze Component Structure

```bash
# Identify what needs testing
# 1. Form validation logic
# 2. User input handling
# 3. API mutation (TanStack Query)
# 4. Success/error handling
# 5. Loading states
# 6. Accessibility
```

### Step 2: Setup Test File

**File**: `src/components/PaymentForm.test.tsx`

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { toast } from 'sonner';
import { PaymentForm } from './PaymentForm';

// Mock external dependencies
vi.mock('sonner', () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
  },
}));

// Test utilities
function renderPaymentForm(props = {}) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  const defaultProps = {
    orderId: 'order-123',
    amount: 99.99,
    onSuccess: vi.fn(),
  };

  return render(
    <QueryClientProvider client={queryClient}>
      <PaymentForm {...defaultProps} {...props} />
    </QueryClientProvider>
  );
}

describe('PaymentForm', () => {
  let fetchMock: any;

  beforeEach(() => {
    // Setup fetch mock
    fetchMock = vi.fn();
    global.fetch = fetchMock;
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  // Tests will be added here...
});
```

### Step 3: Generate Unit Tests (Validation Logic)

```typescript
describe('Form Validation', () => {
  it('should show error for invalid card number', async () => {
    const user = userEvent.setup();
    renderPaymentForm();

    const cardInput = screen.getByLabelText(/card number/i);
    const submitButton = screen.getByRole('button', { name: /pay/i });

    // Enter invalid card (too short)
    await user.type(cardInput, '1234');
    await user.click(submitButton);

    // Should show validation error
    expect(await screen.findByText(/invalid card number/i)).toBeInTheDocument();
  });

  it('should show error for invalid expiry format', async () => {
    const user = userEvent.setup();
    renderPaymentForm();

    const expiryInput = screen.getByLabelText(/expiry/i);
    const submitButton = screen.getByRole('button', { name: /pay/i });

    // Enter invalid expiry
    await user.type(expiryInput, '1234');
    await user.click(submitButton);

    expect(await screen.findByText(/invalid expiry/i)).toBeInTheDocument();
  });

  it('should show error for invalid CVV', async () => {
    const user = userEvent.setup();
    renderPaymentForm();

    const cvvInput = screen.getByLabelText(/cvv/i);
    const submitButton = screen.getByRole('button', { name: /pay/i });

    // Enter invalid CVV (too short)
    await user.type(cvvInput, '12');
    await user.click(submitButton);

    expect(await screen.findByText(/invalid cvv/i)).toBeInTheDocument();
  });

  it('should not submit form when validation fails', async () => {
    const user = userEvent.setup();
    const onSuccess = vi.fn();
    renderPaymentForm({ onSuccess });

    const submitButton = screen.getByRole('button', { name: /pay/i });

    // Submit empty form
    await user.click(submitButton);

    // Should not call API
    expect(fetchMock).not.toHaveBeenCalled();
    expect(onSuccess).not.toHaveBeenCalled();
  });

  it('should clear errors when user corrects input', async () => {
    const user = userEvent.setup();
    renderPaymentForm();

    const cardInput = screen.getByLabelText(/card number/i);
    const submitButton = screen.getByRole('button', { name: /pay/i });

    // Enter invalid card
    await user.type(cardInput, '1234');
    await user.click(submitButton);
    expect(await screen.findByText(/invalid card number/i)).toBeInTheDocument();

    // Correct the input
    await user.clear(cardInput);
    await user.type(cardInput, '1234567890123456');

    // Error should still be visible until next submit
    // (This is a bug found by testing! Should clear on input change)
  });
});
```

### Step 4: Generate Integration Tests (API Calls)

```typescript
describe('Payment Submission', () => {
  it('should successfully process payment', async () => {
    const user = userEvent.setup();
    const onSuccess = vi.fn();

    // Mock successful API response
    fetchMock.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ transactionId: 'txn-456' }),
    });

    renderPaymentForm({ onSuccess });

    // Fill form with valid data
    await user.type(screen.getByLabelText(/card number/i), '1234567890123456');
    await user.type(screen.getByLabelText(/expiry/i), '12/25');
    await user.type(screen.getByLabelText(/cvv/i), '123');

    // Submit
    await user.click(screen.getByRole('button', { name: /pay/i }));

    // Should call API with correct data
    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith('/api/payments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          orderId: 'order-123',
          amount: 99.99,
          cardNumber: '1234567890123456',
          expiry: '12/25',
          cvv: '123',
        }),
      });
    });

    // Should show success toast
    expect(toast.success).toHaveBeenCalledWith('Payment successful!');

    // Should call onSuccess callback
    expect(onSuccess).toHaveBeenCalled();
  });

  it('should handle payment API error', async () => {
    const user = userEvent.setup();

    // Mock API error
    fetchMock.mockResolvedValueOnce({
      ok: false,
      status: 400,
    });

    renderPaymentForm();

    // Fill and submit form
    await user.type(screen.getByLabelText(/card number/i), '1234567890123456');
    await user.type(screen.getByLabelText(/expiry/i), '12/25');
    await user.type(screen.getByLabelText(/cvv/i), '123');
    await user.click(screen.getByRole('button', { name: /pay/i }));

    // Should show error toast
    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith('Payment failed');
    });
  });

  it('should handle network error', async () => {
    const user = userEvent.setup();

    // Mock network failure
    fetchMock.mockRejectedValueOnce(new Error('Network error'));

    renderPaymentForm();

    // Fill and submit form
    await user.type(screen.getByLabelText(/card number/i), '1234567890123456');
    await user.type(screen.getByLabelText(/expiry/i), '12/25');
    await user.type(screen.getByLabelText(/cvv/i), '123');
    await user.click(screen.getByRole('button', { name: /pay/i }));

    // Should show error toast
    await waitFor(() => {
      expect(toast.error).toHaveBeenCalled();
    });
  });
});
```

### Step 5: Generate Loading State Tests

```typescript
describe('Loading States', () => {
  it('should show loading state during payment processing', async () => {
    const user = userEvent.setup();

    // Mock slow API response
    fetchMock.mockImplementationOnce(
      () => new Promise((resolve) => setTimeout(() => resolve({ ok: true, json: async () => ({}) }), 100))
    );

    renderPaymentForm();

    // Fill and submit form
    await user.type(screen.getByLabelText(/card number/i), '1234567890123456');
    await user.type(screen.getByLabelText(/expiry/i), '12/25');
    await user.type(screen.getByLabelText(/cvv/i), '123');
    await user.click(screen.getByRole('button', { name: /pay/i }));

    // Button should show loading state
    expect(screen.getByRole('button', { name: /processing/i })).toBeDisabled();

    // Wait for completion
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /pay/i })).not.toBeDisabled();
    });
  });

  it('should disable form inputs during submission', async () => {
    const user = userEvent.setup();

    // Mock slow API
    fetchMock.mockImplementationOnce(
      () => new Promise((resolve) => setTimeout(() => resolve({ ok: true, json: async () => ({}) }), 100))
    );

    renderPaymentForm();

    await user.type(screen.getByLabelText(/card number/i), '1234567890123456');
    await user.type(screen.getByLabelText(/expiry/i), '12/25');
    await user.type(screen.getByLabelText(/cvv/i), '123');
    await user.click(screen.getByRole('button', { name: /pay/i }));

    // Submit button should be disabled
    expect(screen.getByRole('button')).toBeDisabled();

    await waitFor(() => {
      expect(screen.getByRole('button')).not.toBeDisabled();
    });
  });
});
```

### Step 6: Generate Accessibility Tests

```typescript
describe('Accessibility', () => {
  it('should have proper ARIA labels', () => {
    renderPaymentForm();

    expect(screen.getByLabelText(/card number/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/expiry/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/cvv/i)).toBeInTheDocument();
  });

  it('should associate errors with inputs via aria-describedby', async () => {
    const user = userEvent.setup();
    renderPaymentForm();

    const cardInput = screen.getByLabelText(/card number/i);
    await user.click(screen.getByRole('button', { name: /pay/i }));

    await waitFor(() => {
      expect(cardInput).toHaveAttribute('aria-invalid', 'true');
      expect(cardInput).toHaveAttribute('aria-describedby', 'cardNumber-error');
    });
  });

  it('should announce errors to screen readers', async () => {
    const user = userEvent.setup();
    renderPaymentForm();

    await user.click(screen.getByRole('button', { name: /pay/i }));

    // Error messages should have role="alert"
    const errors = await screen.findAllByRole('alert');
    expect(errors.length).toBeGreaterThan(0);
  });

  it('should support keyboard navigation', async () => {
    const user = userEvent.setup();
    renderPaymentForm();

    // Tab through form
    await user.tab();
    expect(screen.getByLabelText(/card number/i)).toHaveFocus();

    await user.tab();
    expect(screen.getByLabelText(/expiry/i)).toHaveFocus();

    await user.tab();
    expect(screen.getByLabelText(/cvv/i)).toHaveFocus();

    await user.tab();
    expect(screen.getByRole('button', { name: /pay/i })).toHaveFocus();

    // Submit with Enter
    await user.keyboard('{Enter}');
    // Should trigger validation
  });
});
```

### Step 7: Generate Edge Case Tests

```typescript
describe('Edge Cases', () => {
  it('should handle very long card numbers gracefully', async () => {
    const user = userEvent.setup();
    renderPaymentForm();

    const cardInput = screen.getByLabelText(/card number/i);

    // Try to enter 20 digits (should stop at 16)
    await user.type(cardInput, '12345678901234567890');

    expect(cardInput).toHaveValue('1234567890123456');
  });

  it('should format expiry date automatically', async () => {
    const user = userEvent.setup();
    renderPaymentForm();

    const expiryInput = screen.getByLabelText(/expiry/i);

    // User types 1225, should format to 12/25
    // (Bug found: not currently implemented!)
    await user.type(expiryInput, '1225');

    expect(expiryInput).toHaveValue('12/25');
  });

  it('should prevent duplicate submissions', async () => {
    const user = userEvent.setup();

    fetchMock.mockResolvedValue({
      ok: true,
      json: async () => ({ transactionId: 'txn-456' }),
    });

    renderPaymentForm();

    // Fill form
    await user.type(screen.getByLabelText(/card number/i), '1234567890123456');
    await user.type(screen.getByLabelText(/expiry/i), '12/25');
    await user.type(screen.getByLabelText(/cvv/i), '123');

    // Click submit multiple times rapidly
    const submitButton = screen.getByRole('button', { name: /pay/i });
    await user.click(submitButton);
    await user.click(submitButton);
    await user.click(submitButton);

    // Should only call API once
    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledTimes(1);
    });
  });
});
```

## Results

### Coverage Report

```bash
npm run test:coverage

File                   | % Stmts | % Branch | % Funcs | % Lines
-------------------|---------|----------|---------|--------
PaymentForm.tsx    | 100     | 100      | 100     | 100

Test Suites: 1 passed, 1 total
Tests:       42 passed, 42 total
Time:        3.142s
```

### Bugs Found During Testing

1. **Validation errors don't clear on input change**
   - Expected: Errors clear when user starts typing
   - Actual: Errors persist until next submit
   - Fix: Add error clearing to input onChange handlers

2. **No automatic expiry formatting**
   - Expected: Auto-format "1225" → "12/25"
   - Actual: User must type slash manually
   - Fix: Add formatting logic to expiry input

3. **Missing duplicate submission prevention**
   - Expected: Button disabled prevents duplicate API calls
   - Actual: Fast clicks can trigger multiple submissions
   - Test passed (TanStack Query handles this), but good to verify

### Test Organization

```
PaymentForm.test.tsx (42 tests)
├── Form Validation (5 tests)
├── Payment Submission (3 tests)
├── Loading States (2 tests)
├── Accessibility (4 tests)
└── Edge Cases (3 tests)
```

### Time Investment

- Analysis: 15 minutes
- Test writing: 2 hours
- Bug fixes from tests: 30 minutes
- **Total**: 2 hours 45 minutes
- **Value**: Prevented 3 production bugs, 100% coverage

---

Related: [API Endpoint Testing](api-endpoint-testing.md) | [Test Coverage Workflow](test-coverage-workflow.md) | [Return to INDEX](INDEX.md)
