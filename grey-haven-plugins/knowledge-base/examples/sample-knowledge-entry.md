---
uuid: 550e8400-e29b-41d4-a716-446655440000
type: patterns
title: Circuit Breaker Pattern for Microservices
tags: [microservices, resilience, circuit-breaker, fault-tolerance, patterns]
created: 2025-11-10T08:00:00Z
updated: 2025-11-10T08:00:00Z
status: active
relations:
  - slug: retry-pattern-api-calls
    type: references
  - slug: api-resilience-strategy
    type: implements
  - slug: microservices-architecture
    type: part-of
---

# Circuit Breaker Pattern for Microservices

## Overview

The Circuit Breaker pattern prevents cascading failures in distributed systems by monitoring service calls and "opening the circuit" when failure rates exceed thresholds. This pattern is essential for building resilient microservices that gracefully handle downstream service failures.

## Problem Statement

In microservices architectures, when a downstream service becomes unavailable or slow:
- Upstream services waste resources waiting for timeouts
- Thread pools become exhausted
- Failures cascade through the system
- Recovery is difficult even after the downstream service recovers

## Solution

Implement a circuit breaker that wraps service calls and monitors their success/failure:

1. **Closed State** (Normal Operation)
   - All requests pass through
   - Failures are counted
   - If failure threshold exceeded → Open

2. **Open State** (Fast Fail)
   - Requests fail immediately without calling downstream
   - Prevents resource exhaustion
   - After timeout period → Half-Open

3. **Half-Open State** (Recovery Test)
   - Limited requests allowed through
   - If successful → Closed
   - If failed → Open

## Implementation Example

```python
from enum import Enum
from datetime import datetime, timedelta
import time

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold=5,
        timeout_duration=60,
        expected_exception=Exception
    ):
        self.failure_threshold = failure_threshold
        self.timeout_duration = timeout_duration
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _should_attempt_reset(self):
        return (
            datetime.now() - self.last_failure_time
            > timedelta(seconds=self.timeout_duration)
        )

# Usage
breaker = CircuitBreaker(failure_threshold=5, timeout_duration=60)

def call_external_service():
    # Your service call here
    pass

try:
    result = breaker.call(call_external_service)
except Exception as e:
    # Handle circuit open or service failure
    pass
```

## Configuration Parameters

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| `failure_threshold` | Failures before opening circuit | 5-10 |
| `timeout_duration` | Seconds before attempting reset | 30-60s |
| `success_threshold` | Successes needed to close (half-open) | 2-5 |
| `half_open_requests` | Max concurrent requests in half-open | 1-3 |

## Integration with Other Patterns

This pattern works well with:
- [[retry-pattern-api-calls]]: Retry before opening circuit
- [[rate-limiting-strategy]]: Limit requests to struggling services
- [[bulkhead-pattern]]: Isolate resources per service
- [[fallback-pattern]]: Provide default responses when open

## Monitoring and Metrics

Essential metrics to track:
- Circuit state changes (closed → open → half-open)
- Time spent in each state
- Failure rates per endpoint
- Recovery times
- Request volumes blocked

## Common Pitfalls

1. **Threshold Too Low**: Circuit opens too frequently
2. **Timeout Too Short**: Doesn't allow service to recover
3. **No Fallback**: Poor user experience when circuit opens
4. **Shared State**: Use per-instance circuit breakers
5. **No Monitoring**: Can't diagnose or tune behavior

## Related Patterns

- [[retry-pattern-api-calls]]
- [[rate-limiting-strategy]]
- [[bulkhead-pattern]]
- [[fallback-pattern]]
- [[timeout-pattern]]

## References

- Martin Fowler: [Circuit Breaker](https://martinfowler.com/bliki/CircuitBreaker.html)
- Netflix Hystrix: [How It Works](https://github.com/Netflix/Hystrix/wiki/How-it-Works)
- Release It! by Michael Nygard

## Decision Context

**When we implemented this**: October 2025

**Why we chose this pattern**: Experiencing cascading failures when payment service went down

**Alternatives considered**:
- Simple timeouts (insufficient protection)
- Retry only (made problems worse)
- Manual service disable (slow to respond)

## Lessons Learned

1. Start with conservative thresholds
2. Monitor and tune based on actual behavior
3. Always implement fallback behavior
4. Use separate circuit breakers per dependency
5. Log state changes for debugging

---

**Status**: Active and in production
**Maintainer**: Platform Team
**Last Reviewed**: 2025-11-10
