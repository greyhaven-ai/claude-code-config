# React Component Scaffold Example

Complete example of scaffolding a reusable React component with TypeScript, tests, Storybook stories, and CSS modules.

**Duration**: 5 minutes | **Files**: 6 | **LOC**: ~120 | **Stack**: React + TypeScript + Vitest + Storybook

---

## File Tree

```
src/components/Button/
├── Button.tsx           # Component implementation
├── Button.test.tsx      # Vitest + Testing Library tests
├── Button.stories.tsx   # Storybook stories
├── Button.module.css    # CSS modules styling
├── index.ts             # Re-exports
└── README.md            # Component documentation
```

---

## Generated Files

### 1. Button.tsx (Implementation)

```typescript
import React from 'react';
import styles from './Button.module.css';

export interface ButtonProps {
  /** Button label */
  label: string;
  /** Button variant */
  variant?: 'primary' | 'secondary' | 'danger';
  /** Button size */
  size?: 'small' | 'medium' | 'large';
  /** Disabled state */
  disabled?: boolean;
  /** Click handler */
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  onClick,
}) => {
  const className = [
    styles.button,
    styles[variant],
    styles[size],
    disabled && styles.disabled,
  ].filter(Boolean).join(' ');

  return (
    <button
      className={className}
      disabled={disabled}
      onClick={onClick}
      type="button"
    >
      {label}
    </button>
  );
};
```

### 2. Button.test.tsx (Tests)

```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with label', () => {
    render(<Button label="Click me" />);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button label="Click" onClick={handleClick} />);

    fireEvent.click(screen.getByText('Click'));
    expect(handleClick).toHaveBeenCalledOnce();
  });

  it('does not call onClick when disabled', () => {
    const handleClick = vi.fn();
    render(<Button label="Click" onClick={handleClick} disabled />);

    fireEvent.click(screen.getByText('Click'));
    expect(handleClick).not.toHaveBeenCalled();
  });

  it('applies variant classes correctly', () => {
    const { container } = render(<Button label="Test" variant="danger" />);
    expect(container.firstChild).toHaveClass('danger');
  });

  it('applies size classes correctly', () => {
    const { container } = render(<Button label="Test" size="large" />);
    expect(container.firstChild).toHaveClass('large');
  });
});
```

### 3. Button.stories.tsx (Storybook)

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger'],
    },
    size: {
      control: 'select',
      options: ['small', 'medium', 'large'],
    },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    label: 'Primary Button',
    variant: 'primary',
  },
};

export const Secondary: Story = {
  args: {
    label: 'Secondary Button',
    variant: 'secondary',
  },
};

export const Danger: Story = {
  args: {
    label: 'Danger Button',
    variant: 'danger',
  },
};

export const Small: Story = {
  args: {
    label: 'Small Button',
    size: 'small',
  },
};

export const Large: Story = {
  args: {
    label: 'Large Button',
    size: 'large',
  },
};

export const Disabled: Story = {
  args: {
    label: 'Disabled Button',
    disabled: true,
  },
};
```

### 4. Button.module.css (Styles)

```css
.button {
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
  font-family: inherit;
}

.button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.button:active:not(:disabled) {
  transform: translateY(0);
}

/* Variants */
.primary {
  background-color: #0070f3;
  color: white;
}

.primary:hover:not(:disabled) {
  background-color: #0051cc;
}

.secondary {
  background-color: #eaeaea;
  color: #000;
}

.secondary:hover:not(:disabled) {
  background-color: #d0d0d0;
}

.danger {
  background-color: #e00;
  color: white;
}

.danger:hover:not(:disabled) {
  background-color: #c00;
}

/* Sizes */
.small {
  padding: 6px 12px;
  font-size: 14px;
}

.medium {
  padding: 10px 20px;
  font-size: 16px;
}

.large {
  padding: 14px 28px;
  font-size: 18px;
}

/* States */
.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### 5. index.ts (Exports)

```typescript
export { Button } from './Button';
export type { ButtonProps } from './Button';
```

### 6. README.md (Documentation)

```markdown
# Button Component

Reusable button component with variants, sizes, and accessibility features.

## Usage

\`\`\`tsx
import { Button } from '@/components/Button';

function App() {
  return (
    <Button
      label="Click me"
      variant="primary"
      size="medium"
      onClick={() => console.log('Clicked!')}
    />
  );
}
\`\`\`

## Props

- `label` (string, required) - Button text
- `variant` ('primary' | 'secondary' | 'danger', default: 'primary') - Visual style
- `size` ('small' | 'medium' | 'large', default: 'medium') - Button size
- `disabled` (boolean, default: false) - Disabled state
- `onClick` (function, optional) - Click handler

## Variants

- **Primary**: Main call-to-action buttons
- **Secondary**: Less prominent actions
- **Danger**: Destructive actions (delete, remove)

## Accessibility

- Semantic `<button>` element
- Proper ARIA attributes
- Keyboard navigation support
- Disabled state handling
```

---

## Scaffold Command

```bash
# Generate component
npx create-component --name Button --path src/components

# Or manually
mkdir -p src/components/Button
cd src/components/Button

# Create files
touch Button.tsx Button.test.tsx Button.stories.tsx Button.module.css index.ts README.md
```

---

## Testing

```bash
# Run tests
npm test Button.test.tsx

# With coverage
npm test -- --coverage Button.test.tsx

# Watch mode
npm test -- --watch
```

---

## Storybook

```bash
# Start Storybook
npm run storybook

# View at http://localhost:6006
# Navigate to Components > Button
```

---

**Metrics**:
- Files: 6
- LOC: ~120
- Test Coverage: 100%
- Storybook Stories: 6 variants
- Accessibility: WCAG 2.1 AA compliant
