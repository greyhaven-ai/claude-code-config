#!/bin/bash
# React Component Scaffold Generator
# Generates a production-ready React component with tests, Storybook, and CSS modules

set -e

COMPONENT_NAME="${1}"

if [ -z "$COMPONENT_NAME" ]; then
    echo "Usage: $0 ComponentName"
    echo "Example: $0 Button"
    exit 1
fi

# Convert to kebab-case for file names
KEBAB_NAME=$(echo "$COMPONENT_NAME" | sed 's/\([A-Z]\)/-\1/g' | sed 's/^-//' | tr '[:upper:]' '[:lower:]')

echo "🎨 Creating React component: $COMPONENT_NAME ($KEBAB_NAME)"

# Create directory structure
mkdir -p "src/components/$COMPONENT_NAME"
cd "src/components/$COMPONENT_NAME"

# Create component file
cat > "$COMPONENT_NAME.tsx" <<EOF
import React from 'react';
import styles from './$COMPONENT_NAME.module.css';

export interface ${COMPONENT_NAME}Props {
  /** The content to display */
  children?: React.ReactNode;
  /** Additional CSS class names */
  className?: string;
  /** Whether the component is disabled */
  disabled?: boolean;
  /** Click handler */
  onClick?: () => void;
}

/**
 * $COMPONENT_NAME component
 *
 * A reusable component for...
 *
 * @example
 * \`\`\`tsx
 * <$COMPONENT_NAME onClick={() => console.log('clicked')}>
 *   Click me
 * </$COMPONENT_NAME>
 * \`\`\`
 */
export const $COMPONENT_NAME: React.FC<${COMPONENT_NAME}Props> = ({
  children,
  className = '',
  disabled = false,
  onClick,
}) => {
  const handleClick = () => {
    if (!disabled && onClick) {
      onClick();
    }
  };

  return (
    <div
      className={\`\${styles.${KEBAB_NAME}} \${className} \${disabled ? styles.disabled : ''}\`}
      onClick={handleClick}
      role="button"
      tabIndex={disabled ? -1 : 0}
      aria-disabled={disabled}
    >
      {children}
    </div>
  );
};

$COMPONENT_NAME.displayName = '$COMPONENT_NAME';
EOF

# Create CSS module
cat > "$COMPONENT_NAME.module.css" <<EOF
.$KEBAB_NAME {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color, #ccc);
  border-radius: 0.25rem;
  background-color: var(--bg-color, #fff);
  color: var(--text-color, #333);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.$KEBAB_NAME:hover:not(.disabled) {
  background-color: var(--bg-hover-color, #f5f5f5);
  border-color: var(--border-hover-color, #999);
}

.$KEBAB_NAME:focus-visible {
  outline: 2px solid var(--focus-color, #0066ff);
  outline-offset: 2px;
}

.$KEBAB_NAME.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
EOF

# Create index file
cat > "index.ts" <<EOF
export { $COMPONENT_NAME } from './$COMPONENT_NAME';
export type { ${COMPONENT_NAME}Props } from './$COMPONENT_NAME';
EOF

# Create test file
cat > "$COMPONENT_NAME.test.tsx" <<EOF
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { $COMPONENT_NAME } from './$COMPONENT_NAME';

describe('$COMPONENT_NAME', () => {
  it('renders children correctly', () => {
    render(<$COMPONENT_NAME>Test Content</$COMPONENT_NAME>);
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<$COMPONENT_NAME onClick={handleClick}>Click me</$COMPONENT_NAME>);

    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('does not call onClick when disabled', () => {
    const handleClick = vi.fn();
    render(
      <$COMPONENT_NAME onClick={handleClick} disabled>
        Click me
      </$COMPONENT_NAME>
    );

    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).not.toHaveBeenCalled();
  });

  it('applies custom className', () => {
    const { container } = render(
      <$COMPONENT_NAME className="custom-class">Test</$COMPONENT_NAME>
    );

    const element = container.firstChild;
    expect(element).toHaveClass('custom-class');
  });

  it('has correct accessibility attributes', () => {
    render(<$COMPONENT_NAME>Test</$COMPONENT_NAME>);
    const element = screen.getByRole('button');

    expect(element).toHaveAttribute('tabIndex', '0');
    expect(element).toHaveAttribute('aria-disabled', 'false');
  });

  it('has correct accessibility attributes when disabled', () => {
    render(<$COMPONENT_NAME disabled>Test</$COMPONENT_NAME>);
    const element = screen.getByRole('button');

    expect(element).toHaveAttribute('tabIndex', '-1');
    expect(element).toHaveAttribute('aria-disabled', 'true');
  });
});
EOF

# Create Storybook story
cat > "$COMPONENT_NAME.stories.tsx" <<EOF
import type { Meta, StoryObj } from '@storybook/react';
import { $COMPONENT_NAME } from './$COMPONENT_NAME';

const meta = {
  title: 'Components/$COMPONENT_NAME',
  component: $COMPONENT_NAME,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    onClick: { action: 'clicked' },
    disabled: { control: 'boolean' },
    className: { control: 'text' },
  },
} satisfies Meta<typeof $COMPONENT_NAME>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: 'Default $COMPONENT_NAME',
  },
};

export const Disabled: Story = {
  args: {
    children: 'Disabled $COMPONENT_NAME',
    disabled: true,
  },
};

export const WithClick: Story = {
  args: {
    children: 'Click me',
    onClick: () => console.log('Clicked!'),
  },
};

export const CustomClass: Story = {
  args: {
    children: 'Custom Styled',
    className: 'custom-component-class',
  },
};
EOF

# Create README
cat > "README.md" <<EOF
# $COMPONENT_NAME

A reusable React component.

## Usage

\`\`\`tsx
import { $COMPONENT_NAME } from './components/$COMPONENT_NAME';

function MyApp() {
  return (
    <$COMPONENT_NAME onClick={() => console.log('clicked')}>
      Click me
    </$COMPONENT_NAME>
  );
}
\`\`\`

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| \`children\` | \`React.ReactNode\` | - | The content to display |
| \`className\` | \`string\` | \`''\` | Additional CSS class names |
| \`disabled\` | \`boolean\` | \`false\` | Whether the component is disabled |
| \`onClick\` | \`() => void\` | - | Click handler |

## Testing

\`\`\`bash
npm test -- $COMPONENT_NAME.test.tsx
\`\`\`

## Storybook

\`\`\`bash
npm run storybook
# View at http://localhost:6006/?path=/story/components-${KEBAB_NAME}
\`\`\`

## Accessibility

- Uses semantic HTML with \`role="button"\`
- Keyboard accessible with \`tabIndex\`
- Screen reader friendly with \`aria-disabled\`
- Focus visible with outline

## CSS Variables

Customize the component by overriding CSS variables:

\`\`\`css
.$KEBAB_NAME {
  --bg-color: #fff;
  --bg-hover-color: #f5f5f5;
  --border-color: #ccc;
  --border-hover-color: #999;
  --text-color: #333;
  --focus-color: #0066ff;
}
\`\`\`
EOF

cd ../../..

echo "✅ React component created: src/components/$COMPONENT_NAME"
echo ""
echo "Files created:"
echo "  - $COMPONENT_NAME.tsx (component)"
echo "  - $COMPONENT_NAME.module.css (styles)"
echo "  - $COMPONENT_NAME.test.tsx (tests)"
echo "  - $COMPONENT_NAME.stories.tsx (Storybook)"
echo "  - index.ts (exports)"
echo "  - README.md (documentation)"
echo ""
echo "Next steps:"
echo "  1. Import: import { $COMPONENT_NAME } from './components/$COMPONENT_NAME';"
echo "  2. Test: npm test -- $COMPONENT_NAME.test.tsx"
echo "  3. View in Storybook: npm run storybook"
