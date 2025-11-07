# TanStack Query Configuration

QueryClient configuration reference for Grey Haven projects.

## Default Configuration

```typescript
import { QueryClient } from "@tanstack/react-query";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60000, // 1 minute
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
```

## Configuration Options

### Query Options

| Option | Default | Description |
|--------|---------|-------------|
| `staleTime` | 60000ms | How long data stays fresh |
| `retry` | 1 | Number of retry attempts |
| `refetchOnWindowFocus` | false | Refetch when window gains focus |
| `refetchInterval` | false | Auto-refetch interval |
| `enabled` | true | Whether query runs automatically |

### Mutation Options

| Option | Default | Description |
|--------|---------|-------------|
| `retry` | 0 | Number of retry attempts |
| `onSuccess` | undefined | Success callback |
| `onError` | undefined | Error callback |
| `onSettled` | undefined | Always runs after success/error |

## Per-Query Configuration

```typescript
const { data } = useQuery({
  queryKey: ["user", userId],
  queryFn: () => getUserById(userId),
  staleTime: 300000, // Override default (5 minutes)
  retry: 3, // Override default
  refetchOnWindowFocus: true, // Override default
});
```

## DevTools Setup

```typescript
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

function RootComponent() {
  return (
    <QueryClientProvider client={queryClient}>
      <App />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```
