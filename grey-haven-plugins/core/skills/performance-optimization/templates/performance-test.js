/**
 * Performance Test Template
 * 
 * Benchmark functions to measure optimization impact.
 */

// Benchmark function
function benchmark(fn, iterations = 1000) {
  const start = performance.now();
  
  for (let i = 0; i < iterations; i++) {
    fn();
  }
  
  const end = performance.now();
  const total = end - start;
  const avg = total / iterations;
  
  return {
    total: total.toFixed(2),
    average: avg.toFixed(4),
    iterations
  };
}

// Example: Before optimization
function processItemsOld(items) {
  const result = [];
  for (let i = 0; i < items.length; i++) {
    for (let j = 0; j < items.length; j++) {
      if (items[i].id === items[j].relatedId) {
        result.push({ item: items[i], related: items[j] });
      }
    }
  }
  return result;
}

// Example: After optimization
function processItemsNew(items) {
  const map = new Map(items.map(i => [i.id, i]));
  return items
    .filter(i => i.relatedId)
    .map(i => ({ item: i, related: map.get(i.relatedId) }));
}

// Test data
const testItems = Array.from({ length: 1000 }, (_, i) => ({
  id: i,
  relatedId: Math.floor(Math.random() * 1000)
}));

// Run benchmarks
console.log('Performance Benchmark Results\n');

const oldResults = benchmark(() => processItemsOld(testItems), 100);
console.log('Before Optimization:');
console.log(`  Total: ${oldResults.total}ms`);
console.log(`  Average: ${oldResults.average}ms`);
console.log(`  Iterations: ${oldResults.iterations}\n`);

const newResults = benchmark(() => processItemsNew(testItems), 100);
console.log('After Optimization:');
console.log(`  Total: ${newResults.total}ms`);
console.log(`  Average: ${newResults.average}ms`);
console.log(`  Iterations: ${newResults.iterations}\n`);

const improvement = ((parseFloat(oldResults.total) / parseFloat(newResults.total))).toFixed(1);
console.log(`Performance Gain: ${improvement}x faster`);
