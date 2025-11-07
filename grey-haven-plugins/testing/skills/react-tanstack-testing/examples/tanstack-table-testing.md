# TanStack Table Testing Examples

Complete examples for testing TanStack Table sorting, filtering, pagination, and selection.

## Test Setup

### Sample Data

```typescript
// src/test/table-data.ts
export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  age: number;
}

export const mockUsers: User[] = [
  { id: '1', name: 'Alice', email: 'alice@example.com', role: 'Admin', age: 30 },
  { id: '2', name: 'Bob', email: 'bob@example.com', role: 'User', age: 25 },
  { id: '3', name: 'Charlie', email: 'charlie@example.com', role: 'User', age: 35 },
  { id: '4', name: 'Diana', email: 'diana@example.com', role: 'Admin', age: 28 },
];
```

## Example 1: Testing Table Rendering

### Basic Table Component

```typescript
// src/components/UserTable.tsx
import { useReactTable, getCoreRowModel, flexRender, ColumnDef } from '@tanstack/react-table';
import { User } from '../test/table-data';

interface UserTableProps {
  data: User[];
}

export function UserTable({ data }: UserTableProps) {
  const columns: ColumnDef<User>[] = [
    {
      accessorKey: 'name',
      header: 'Name',
    },
    {
      accessorKey: 'email',
      header: 'Email',
    },
    {
      accessorKey: 'role',
      header: 'Role',
    },
    {
      accessorKey: 'age',
      header: 'Age',
    },
  ];

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <table>
      <thead>
        {table.getHeaderGroups().map((headerGroup) => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map((header) => (
              <th key={header.id}>
                {flexRender(header.column.columnDef.header, header.getContext())}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
        {table.getRowModel().rows.map((row) => (
          <tr key={row.id}>
            {row.getVisibleCells().map((cell) => (
              <td key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### Test Suite

```typescript
// src/components/UserTable.test.tsx
import { describe, it, expect } from 'vitest';
import { screen, render } from '@testing-library/react';
import { UserTable } from './UserTable';
import { mockUsers } from '../test/table-data';

describe('UserTable', () => {
  it('renders table headers', () => {
    render(<UserTable data={mockUsers} />);

    expect(screen.getByRole('columnheader', { name: 'Name' })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: 'Email' })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: 'Role' })).toBeInTheDocument();
    expect(screen.getByRole('columnheader', { name: 'Age' })).toBeInTheDocument();
  });

  it('renders all user data', () => {
    render(<UserTable data={mockUsers} />);

    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('alice@example.com')).toBeInTheDocument();
    expect(screen.getByText('Bob')).toBeInTheDocument();
    expect(screen.getByText('bob@example.com')).toBeInTheDocument();
  });

  it('renders correct number of rows', () => {
    render(<UserTable data={mockUsers} />);

    const rows = screen.getAllByRole('row');
    expect(rows).toHaveLength(5); // 1 header + 4 data rows
  });
});
```

## Example 2: Testing Sorting

### Table with Sorting

```typescript
// src/components/SortableTable.tsx
import { useReactTable, getCoreRowModel, getSortedRowModel, flexRender, SortingState } from '@tanstack/react-table';
import { useState } from 'react';

export function SortableTable({ data, columns }) {
  const [sorting, setSorting] = useState<SortingState>([]);

  const table = useReactTable({
    data,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <table>
      <thead>
        {table.getHeaderGroups().map((headerGroup) => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map((header) => (
              <th key={header.id}>
                {header.isPlaceholder ? null : (
                  <button
                    onClick={header.column.getToggleSortingHandler()}
                    aria-label={`Sort by ${header.column.id}`}
                  >
                    {flexRender(header.column.columnDef.header, header.getContext())}
                    {{
                      asc: ' 🔼',
                      desc: ' 🔽',
                    }[header.column.getIsSorted() as string] ?? null}
                  </button>
                )}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
        {table.getRowModel().rows.map((row) => (
          <tr key={row.id}>
            {row.getVisibleCells().map((cell) => (
              <td key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### Test Suite

```typescript
// src/components/SortableTable.test.tsx
import { describe, it, expect } from 'vitest';
import { screen, render, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SortableTable } from './SortableTable';
import { mockUsers } from '../test/table-data';

const columns = [
  { accessorKey: 'name', header: 'Name' },
  { accessorKey: 'age', header: 'Age' },
];

describe('SortableTable', () => {
  it('sorts by name ascending', async () => {
    const user = userEvent.setup();
    render(<SortableTable data={mockUsers} columns={columns} />);

    // Click name header to sort
    await user.click(screen.getByRole('button', { name: 'Sort by name' }));

    const rows = screen.getAllByRole('row');
    const firstDataRow = rows[1]; // Skip header row

    expect(within(firstDataRow).getByText('Alice')).toBeInTheDocument();
  });

  it('sorts by name descending on second click', async () => {
    const user = userEvent.setup();
    render(<SortableTable data={mockUsers} columns={columns} />);

    const sortButton = screen.getByRole('button', { name: 'Sort by name' });

    // First click: ascending
    await user.click(sortButton);

    // Second click: descending
    await user.click(sortButton);

    const rows = screen.getAllByRole('row');
    const firstDataRow = rows[1];

    expect(within(firstDataRow).getByText('Diana')).toBeInTheDocument();
  });

  it('sorts by age correctly', async () => {
    const user = userEvent.setup();
    render(<SortableTable data={mockUsers} columns={columns} />);

    await user.click(screen.getByRole('button', { name: 'Sort by age' }));

    const rows = screen.getAllByRole('row');
    const ages = rows.slice(1).map((row) => parseInt(within(row).getAllByRole('cell')[1].textContent || '0'));

    expect(ages).toEqual([25, 28, 30, 35]); // Sorted ascending
  });
});
```

## Example 3: Testing Pagination

### Table with Pagination

```typescript
// src/components/PaginatedTable.tsx
import { useReactTable, getCoreRowModel, getPaginationRowModel, flexRender } from '@tanstack/react-table';

export function PaginatedTable({ data, columns }) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: {
      pagination: {
        pageSize: 2,
      },
    },
  });

  return (
    <div>
      <table>
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th key={header.id}>
                  {flexRender(header.column.columnDef.header, header.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      <div>
        <button
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          Previous
        </button>
        <span>
          Page {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}
        </span>
        <button
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          Next
        </button>
      </div>
    </div>
  );
}
```

### Test Suite

```typescript
// src/components/PaginatedTable.test.tsx
import { describe, it, expect } from 'vitest';
import { screen, render } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { PaginatedTable } from './PaginatedTable';
import { mockUsers } from '../test/table-data';

const columns = [
  { accessorKey: 'name', header: 'Name' },
];

describe('PaginatedTable', () => {
  it('displays first page of results', () => {
    render(<PaginatedTable data={mockUsers} columns={columns} />);

    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('Bob')).toBeInTheDocument();
    expect(screen.queryByText('Charlie')).not.toBeInTheDocument();
  });

  it('navigates to next page', async () => {
    const user = userEvent.setup();
    render(<PaginatedTable data={mockUsers} columns={columns} />);

    await user.click(screen.getByRole('button', { name: 'Next' }));

    expect(screen.queryByText('Alice')).not.toBeInTheDocument();
    expect(screen.getByText('Charlie')).toBeInTheDocument();
    expect(screen.getByText('Diana')).toBeInTheDocument();
  });

  it('displays correct page number', async () => {
    const user = userEvent.setup();
    render(<PaginatedTable data={mockUsers} columns={columns} />);

    expect(screen.getByText('Page 1 of 2')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Next' }));

    expect(screen.getByText('Page 2 of 2')).toBeInTheDocument();
  });

  it('disables previous button on first page', () => {
    render(<PaginatedTable data={mockUsers} columns={columns} />);

    expect(screen.getByRole('button', { name: 'Previous' })).toBeDisabled();
  });

  it('disables next button on last page', async () => {
    const user = userEvent.setup();
    render(<PaginatedTable data={mockUsers} columns={columns} />);

    await user.click(screen.getByRole('button', { name: 'Next' }));

    expect(screen.getByRole('button', { name: 'Next' })).toBeDisabled();
  });
});
```

## Example 4: Testing Row Selection

### Table with Row Selection

```typescript
// src/components/SelectableTable.tsx
import { useReactTable, getCoreRowModel, flexRender, RowSelectionState } from '@tanstack/react-table';
import { useState } from 'react';

export function SelectableTable({ data, columns }) {
  const [rowSelection, setRowSelection] = useState<RowSelectionState>({});

  const table = useReactTable({
    data,
    columns,
    state: { rowSelection },
    onRowSelectionChange: setRowSelection,
    getCoreRowModel: getCoreRowModel(),
    enableRowSelection: true,
  });

  return (
    <div>
      <p data-testid="selected-count">
        {Object.keys(rowSelection).length} selected
      </p>

      <table>
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              <th>
                <input type="checkbox" checked={table.getIsAllRowsSelected()} onChange={table.getToggleAllRowsSelectedHandler()} aria-label="Select all rows" />
              </th>
              {headerGroup.headers.map((header) => (
                <th key={header.id}>{flexRender(header.column.columnDef.header, header.getContext())}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              <td>
                <input
                  type="checkbox"
                  checked={row.getIsSelected()}
                  onChange={row.getToggleSelectedHandler()}
                  aria-label={`Select row ${row.id}`}
                />
              </td>
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

### Test Suite

```typescript
// src/components/SelectableTable.test.tsx
import { describe, it, expect } from 'vitest';
import { screen, render } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SelectableTable } from './SelectableTable';
import { mockUsers } from '../test/table-data';

const columns = [
  { accessorKey: 'name', header: 'Name' },
];

describe('SelectableTable', () => {
  it('selects individual row', async () => {
    const user = userEvent.setup();
    render(<SelectableTable data={mockUsers} columns={columns} />);

    await user.click(screen.getByRole('checkbox', { name: 'Select row 0' }));

    expect(screen.getByTestId('selected-count')).toHaveTextContent('1 selected');
  });

  it('selects all rows', async () => {
    const user = userEvent.setup();
    render(<SelectableTable data={mockUsers} columns={columns} />);

    await user.click(screen.getByRole('checkbox', { name: 'Select all rows' }));

    expect(screen.getByTestId('selected-count')).toHaveTextContent('4 selected');
  });
});
```

## Key Takeaways

1. **Core Setup**: Use `useReactTable` with appropriate row models (core, sorted, pagination)
2. **Sorting**: Test ascending, descending, and unsorted states
3. **Pagination**: Test navigation, disabled states, and page indicators
4. **Selection**: Test individual and bulk selection
5. **Accessibility**: Use proper ARIA labels for buttons and checkboxes

---

**Next**: [TanStack Form Testing](tanstack-form-testing.md) | **Previous**: [Router Testing](tanstack-router-testing.md)
