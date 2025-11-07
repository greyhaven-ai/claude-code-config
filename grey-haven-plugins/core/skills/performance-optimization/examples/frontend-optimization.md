# Frontend Optimization Examples

React and frontend performance optimizations with measurable Web Vitals improvements.

## Example 1: Code Splitting

### Problem: Large Bundle

```typescript
// ❌ BEFORE: Single bundle - 1.2MB JavaScript, 4.5s load time
import { Dashboard } from './Dashboard';
import { Analytics } from './Analytics';
import { Settings } from './Settings';
import { Admin } from './Admin';

function App() {
  return (
    <Router>
      <Route path="/" component={Dashboard} />
      <Route path="/analytics" component={Analytics} />
      <Route path="/settings" component={Settings} />
      <Route path="/admin" component={Admin} />
    </Router>
  );
}

// Initial bundle: 1.2MB
// First Contentful Paint: 4.5s
```

### Solution: Dynamic Imports

```typescript
// ✅ AFTER: Code splitting - 200KB initial, 1.8s load time
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./Dashboard'));
const Analytics = lazy(() => import('./Analytics'));
const Settings = lazy(() => import('./Settings'));
const Admin = lazy(() => import('./Admin'));

function App() {
  return (
    <Router>
      <Suspense fallback={<Loading />}>
        <Route path="/" component={Dashboard} />
        <Route path="/analytics" component={Analytics} />
        <Route path="/settings" component={Settings} />
        <Route path="/admin" component={Admin} />
      </Suspense>
    </Router>
  );
}

// Initial bundle: 200KB (6x smaller)
// First Contentful Paint: 1.8s (2.5x faster)
```

### Metrics

| Implementation | Bundle Size | FCP | LCP |
|----------------|-------------|-----|-----|
| **Single Bundle** | 1.2 MB | 4.5s | 5.2s |
| **Code Split** | 200 KB | 1.8s | 2.1s |
| **Improvement** | **83% less** | **2.5x** | **2.5x** |

---

## Example 2: React Rendering Optimization

### Problem: Unnecessary Re-renders

```typescript
// ❌ BEFORE: Re-renders entire list on every update - 250ms
function ProductList({ products }) {
  const [filter, setFilter] = useState('');
  
  return (
    <>
      <input value={filter} onChange={e => setFilter(e.target.value)} />
      {products.map(product => (
        <ProductCard 
          key={product.id}
          product={product}
          onUpdate={handleUpdate}
        />
      ))}
    </>
  );
}

// Every keystroke: 250ms to re-render 100 items
```

### Solution: Memoization

```typescript
// ✅ AFTER: Memoized components - 15ms per update
const ProductCard = memo(({ product, onUpdate }) => {
  return <div>{product.name}</div>;
});

function ProductList({ products }) {
  const [filter, setFilter] = useState('');
  
  const handleUpdate = useCallback((id, data) => {
    // Update logic
  }, []);
  
  const filteredProducts = useMemo(() => {
    return products.filter(p => p.name.includes(filter));
  }, [products, filter]);
  
  return (
    <>
      <input value={filter} onChange={e => setFilter(e.target.value)} />
      {filteredProducts.map(product => (
        <ProductCard 
          key={product.id}
          product={product}
          onUpdate={handleUpdate}
        />
      ))}
    </>
  );
}

// Every keystroke: 15ms (17x faster)
```

---

## Example 3: Virtual Scrolling

### Problem: Rendering Large Lists

```typescript
// ❌ BEFORE: Render all 10,000 items - 8s initial render
function UserList({ users }) {
  return (
    <div>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}

// 10,000 DOM nodes created
// Initial render: 8,000ms
// Memory: 450MB
```

### Solution: react-window

```typescript
// ✅ AFTER: Render only visible items - 180ms initial render
import { FixedSizeList } from 'react-window';

function UserList({ users }) {
  const Row = ({ index, style }) => (
    <div style={style}>
      <UserCard user={users[index]} />
    </div>
  );
  
  return (
    <FixedSizeList
      height={600}
      itemCount={users.length}
      itemSize={80}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}

// ~15 DOM nodes created (only visible items)
// Initial render: 180ms (44x faster)
// Memory: 25MB (18x less)
```

---

## Example 4: Image Optimization

### Problem: Large Unoptimized Images

```html
<!-- ❌ BEFORE: 4MB PNG, 3.5s load time -->
<img src="/images/hero.png" alt="Hero" />
```

### Solution: Optimized Formats + Lazy Loading

```html
<!-- ✅ AFTER: 180KB WebP, lazy loaded - 0.4s -->
<picture>
  <source srcset="/images/hero-small.webp" media="(max-width: 640px)" />
  <source srcset="/images/hero-medium.webp" media="(max-width: 1024px)" />
  <source srcset="/images/hero-large.webp" media="(min-width: 1025px)" />
  <img 
    src="/images/hero-large.webp" 
    alt="Hero"
    loading="lazy"
    decoding="async"
  />
</picture>
```

### Metrics

| Implementation | File Size | Load Time | LCP Impact |
|----------------|-----------|-----------|------------|
| **PNG** | 4 MB | 3.5s | 3.8s LCP |
| **WebP + Lazy** | 180 KB | 0.4s | 1.2s LCP |
| **Improvement** | **96% less** | **8.8x** | **3.2x** |

---

## Example 5: Tree Shaking

### Problem: Importing Entire Library

```typescript
// ❌ BEFORE: Imports entire lodash (72KB)
import _ from 'lodash';

const debounced = _.debounce(fn, 300);
const sorted = _.sortBy(arr, 'name');

// Bundle includes all 300+ lodash functions
// Added bundle size: 72KB
```

### Solution: Import Specific Functions

```typescript
// ✅ AFTER: Import only needed functions (4KB)
import debounce from 'lodash-es/debounce';
import sortBy from 'lodash-es/sortBy';

const debounced = debounce(fn, 300);
const sorted = sortBy(arr, 'name');

// Bundle includes only 2 functions
// Added bundle size: 4KB (18x smaller)
```

---

## Summary

| Optimization | Before | After | Gain | Web Vital |
|--------------|--------|-------|------|-----------|
| **Code Splitting** | 1.2MB | 200KB | 6x | FCP, LCP |
| **Memo + useCallback** | 250ms | 15ms | 17x | FID |
| **Virtual Scrolling** | 8s | 180ms | 44x | LCP, CLS |
| **Image Optimization** | 4MB | 180KB | 22x | LCP |
| **Tree Shaking** | 72KB | 4KB | 18x | FCP |

## Web Vitals Targets

- **LCP** (Largest Contentful Paint): <2.5s
- **FID** (First Input Delay): <100ms
- **CLS** (Cumulative Layout Shift): <0.1

---

**Previous**: [Caching Optimization](caching-optimization.md) | **Next**: [Backend Optimization](backend-optimization.md) | **Index**: [Examples Index](INDEX.md)
