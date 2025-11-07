# Large Dataset Memory Optimization

Memory-efficient patterns for processing multi-GB datasets in Python and Node.js without OOM errors.

## Overview

**Before Optimization**:
- Dataset size: 10GB CSV (50M rows)
- Memory usage: 20GB (2x dataset size)
- Processing time: 45 minutes
- OOM errors: Frequent (3-4x/day)

**After Optimization**:
- Dataset size: Same (10GB, 50M rows)
- Memory usage: 500MB (constant)
- Processing time: 12 minutes (73% faster)
- OOM errors: 0/month

**Tools**: Polars, pandas chunking, generators, streaming parsers

## 1. Problem: Loading Entire Dataset

### Vulnerable Pattern (Pandas read_csv)

```python
# analysis.py (BEFORE)
import pandas as pd

def analyze_sales_data(filename: str):
    # ❌ Loads entire 10GB file into memory
    df = pd.read_csv(filename)  # 20GB RAM usage

    # ❌ Creates copies for each operation
    df['total'] = df['quantity'] * df['price']  # +10GB
    df_filtered = df[df['total'] > 1000]  # +8GB
    df_sorted = df_filtered.sort_values('total', ascending=False)  # +8GB

    # Peak memory: 46GB for 10GB file!
    return df_sorted.head(100)
```

**Memory Profile**:
```
Step 1 (read_csv):     20GB
Step 2 (calculation):  +10GB = 30GB
Step 3 (filter):       +8GB  = 38GB
Step 4 (sort):         +8GB  = 46GB
Result: OOM on 32GB machine
```

## 2. Solution 1: Pandas Chunking

### Chunk-Based Processing

```python
# analysis.py (AFTER - Chunking)
import pandas as pd
from typing import Iterator

def analyze_sales_data_chunked(filename: str, chunk_size: int = 100000):
    """Process 100K rows at a time (constant memory)"""

    top_sales = []

    # ✅ Process in chunks (100K rows = ~50MB each)
    for chunk in pd.read_csv(filename, chunksize=chunk_size):
        # Calculate total (in-place when possible)
        chunk['total'] = chunk['quantity'] * chunk['price']

        # Filter high-value sales
        filtered = chunk[chunk['total'] > 1000]

        # Keep top 100 from this chunk
        top_chunk = filtered.nlargest(100, 'total')
        top_sales.append(top_chunk)

        # chunk goes out of scope, memory freed

    # Combine top results from all chunks
    final_df = pd.concat(top_sales).nlargest(100, 'total')
    return final_df
```

**Memory Profile (Chunked)**:
```
Chunk 1: 50MB (process) → 10MB (top 100) → garbage collected
Chunk 2: 50MB (process) → 10MB (top 100) → garbage collected
...
Chunk 500: 50MB (process) → 10MB (top 100) → garbage collected
Final combine: 500 * 10MB = 500MB total
Peak memory: 500MB (99% reduction!)
```

## 3. Solution 2: Polars (Lazy Evaluation)

### Polars for Large Datasets

**Why Polars**:
- 10-100x faster than pandas
- True streaming (doesn't load entire file)
- Query optimizer (like SQL databases)
- Parallel processing (uses all CPU cores)

```python
# analysis.py (POLARS)
import polars as pl

def analyze_sales_data_polars(filename: str):
    """Polars lazy evaluation - constant memory"""

    result = (
        pl.scan_csv(filename)  # ✅ Lazy: doesn't load yet
        .with_columns([
            (pl.col('quantity') * pl.col('price')).alias('total')
        ])
        .filter(pl.col('total') > 1000)
        .sort('total', descending=True)
        .head(100)
        .collect(streaming=True)  # ✅ Streaming: processes in chunks
    )

    return result
```

**Memory Profile (Polars Streaming)**:
```
Memory usage: 200-300MB (constant)
Processing: Parallel chunks, optimized query plan
Time: 12 minutes vs 45 minutes (pandas)
```

## 4. Node.js Streaming

### CSV Streaming with csv-parser

```typescript
// analysis.ts (BEFORE)
import fs from 'fs';
import Papa from 'papaparse';

async function analyzeSalesData(filename: string) {
  // ❌ Loads entire 10GB file
  const fileContent = fs.readFileSync(filename, 'utf-8');  // 20GB RAM
  const parsed = Papa.parse(fileContent, { header: true });  // +10GB

  // Process all rows
  const results = parsed.data.map(row => ({
    total: row.quantity * row.price
  }));

  return results;  // 30GB total
}
```

**Fixed with Streaming**:
```typescript
// analysis.ts (AFTER - Streaming)
import fs from 'fs';
import csv from 'csv-parser';
import { pipeline } from 'stream/promises';

async function analyzeSalesDataStreaming(filename: string) {
  const topSales: Array<{row: any, total: number}> = [];

  await pipeline(
    fs.createReadStream(filename),  // ✅ Stream (not load all)
    csv(),
    async function* (source) {
      for await (const row of source) {
        const total = row.quantity * row.price;

        if (total > 1000) {
          topSales.push({ row, total });

          // Keep only top 100 (memory bounded)
          if (topSales.length > 100) {
            topSales.sort((a, b) => b.total - a.total);
            topSales.length = 100;
          }
        }
      }
      yield topSales;
    }
  );

  return topSales;
}
```

**Memory Profile (Streaming)**:
```
Buffer: 64KB (stream chunk size)
Processing: One row at a time
Array: 100 rows max (bounded)
Peak memory: 5MB vs 30GB (99.98% reduction!)
```

## 5. Generator Pattern (Python)

### Memory-Efficient Pipeline

```python
# pipeline.py (Generator-based)
from typing import Iterator
import csv

def read_csv_streaming(filename: str) -> Iterator[dict]:
    """Read CSV line by line (not all at once)"""
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row  # ✅ One row at a time

def calculate_totals(rows: Iterator[dict]) -> Iterator[dict]:
    """Calculate totals (lazy)"""
    for row in rows:
        row['total'] = float(row['quantity']) * float(row['price'])
        yield row

def filter_high_value(rows: Iterator[dict], threshold: float = 1000) -> Iterator[dict]:
    """Filter high-value sales (lazy)"""
    for row in rows:
        if row['total'] > threshold:
            yield row

def top_n(rows: Iterator[dict], n: int = 100) -> list[dict]:
    """Keep top N rows (bounded memory)"""
    import heapq
    return heapq.nlargest(n, rows, key=lambda x: x['total'])

# ✅ Pipeline: each stage processes one row at a time
def analyze_sales_pipeline(filename: str):
    rows = read_csv_streaming(filename)
    with_totals = calculate_totals(rows)
    high_value = filter_high_value(with_totals)
    top_100 = top_n(high_value, 100)
    return top_100
```

**Memory Profile (Generator Pipeline)**:
```
Stage 1 (read): 1 row (few KB)
Stage 2 (calculate): 1 row (few KB)
Stage 3 (filter): 1 row (few KB)
Stage 4 (top_n): 100 rows (bounded)
Peak memory: <1MB (constant)
```

## 6. Real-World: E-Commerce Analytics

### Before (Pandas load_all)

```python
# analytics_service.py (BEFORE)
import pandas as pd

class AnalyticsService:
    def generate_sales_report(self, start_date: str, end_date: str):
        # ❌ Load entire orders table (10GB)
        orders = pd.read_sql(
            "SELECT * FROM orders WHERE date BETWEEN %s AND %s",
            engine,
            params=(start_date, end_date)
        )  # 20GB RAM

        # ❌ Load entire order_items (50GB)
        items = pd.read_sql("SELECT * FROM order_items", engine)  # +100GB RAM

        # Join (creates another copy)
        merged = orders.merge(items, on='order_id')  # +150GB

        # Aggregate
        summary = merged.groupby('category').agg({
            'total': 'sum',
            'quantity': 'sum'
        })

        return summary  # Peak: 270GB - OOM!
```

### After (Database Aggregation + Chunking)

```python
# analytics_service.py (AFTER)
import pandas as pd

class AnalyticsService:
    def generate_sales_report(self, start_date: str, end_date: str):
        # ✅ Aggregate in database (PostgreSQL does the work)
        query = """
            SELECT
                oi.category,
                SUM(oi.price * oi.quantity) as total,
                SUM(oi.quantity) as quantity
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            WHERE o.date BETWEEN %(start)s AND %(end)s
            GROUP BY oi.category
        """

        # Result: aggregated data (few KB, not 270GB!)
        summary = pd.read_sql(
            query,
            engine,
            params={'start': start_date, 'end': end_date}
        )

        return summary  # Peak: 1MB vs 270GB
```

**Metrics**:
```
Before: 270GB RAM, OOM error
After: 1MB RAM, 99.9996% reduction
Time: 45 min → 30 seconds (90x faster)
```

## 7. Dask for Parallel Processing

### Dask DataFrame (Parallel Chunking)

```python
# analysis_dask.py
import dask.dataframe as dd

def analyze_sales_data_dask(filename: str):
    """Process in parallel chunks across CPU cores"""

    # ✅ Lazy loading, parallel processing
    df = dd.read_csv(
        filename,
        blocksize='64MB'  # Process 64MB chunks
    )

    # All operations are lazy (no computation yet)
    df['total'] = df['quantity'] * df['price']
    filtered = df[df['total'] > 1000]
    top_100 = filtered.nlargest(100, 'total')

    # ✅ Trigger computation (parallel across cores)
    result = top_100.compute()

    return result
```

**Memory Profile (Dask)**:
```
Workers: 8 (one per CPU core)
Memory per worker: 100MB
Total memory: 800MB vs 46GB
Speed: 4-8x faster (parallel)
```

## 8. Memory Monitoring

### Track Memory Usage During Processing

```python
# monitor.py
import tracemalloc
import psutil
from contextlib import contextmanager

@contextmanager
def memory_monitor(label: str):
    """Monitor memory usage of code block"""

    # Start tracking
    tracemalloc.start()
    process = psutil.Process()
    mem_before = process.memory_info().rss / 1024 / 1024  # MB

    yield

    # Measure after
    mem_after = process.memory_info().rss / 1024 / 1024
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"{label}:")
    print(f"  Memory before: {mem_before:.1f} MB")
    print(f"  Memory after: {mem_after:.1f} MB")
    print(f"  Memory delta: {mem_after - mem_before:.1f} MB")
    print(f"  Peak traced: {peak / 1024 / 1024:.1f} MB")

# Usage
with memory_monitor("Pandas load_all"):
    df = pd.read_csv("large_file.csv")  # Shows high memory usage

with memory_monitor("Polars streaming"):
    df = pl.scan_csv("large_file.csv").collect(streaming=True)  # Low memory
```

## 9. Optimization Decision Tree

**Choose the right tool based on dataset size**:

```
Dataset < 1GB:
  → Use pandas.read_csv() (simple, fast)

Dataset 1-10GB:
  → Use pandas chunking (chunksize=100000)
  → Or Polars streaming (faster, less memory)

Dataset 10-100GB:
  → Use Polars streaming (best performance)
  → Or Dask (parallel processing)
  → Or Database aggregation (PostgreSQL, ClickHouse)

Dataset > 100GB:
  → Database aggregation (required)
  → Or Spark/Ray (distributed computing)
  → Never load into memory
```

## 10. Results and Impact

### Before vs After Metrics

| Metric | Before (pandas) | After (Polars) | Impact |
|--------|----------------|----------------|--------|
| **Memory Usage** | 46GB | 300MB | **99.3% reduction** |
| **Processing Time** | 45 min | 12 min | **73% faster** |
| **OOM Errors** | 3-4/day | 0/month | **100% eliminated** |
| **Max Dataset Size** | 10GB | 500GB+ | **50x scalability** |

### Key Optimizations Applied

1. **Chunking**: Process 100K rows at a time (constant memory)
2. **Lazy Evaluation**: Polars/Dask don't load until needed
3. **Streaming**: One row at a time (generators, Node.js streams)
4. **Database Aggregation**: Let PostgreSQL do the work
5. **Bounded Memory**: heapq.nlargest() keeps top N (not all rows)

### Cost Savings

**Infrastructure costs**:
- Before: r5.8xlarge (256GB RAM) = $1.344/hour
- After: r5.large (16GB RAM) = $0.084/hour
- **Savings**: 94% reduction ($23,000/year per service)

## Related Documentation

- **Node.js Leaks**: [nodejs-memory-leak.md](nodejs-memory-leak.md)
- **Python Profiling**: [python-scalene-profiling.md](python-scalene-profiling.md)
- **DB Leaks**: [database-connection-leak.md](database-connection-leak.md)
- **Reference**: [../reference/memory-optimization-patterns.md](../reference/memory-optimization-patterns.md)

---

Return to [examples index](INDEX.md)
