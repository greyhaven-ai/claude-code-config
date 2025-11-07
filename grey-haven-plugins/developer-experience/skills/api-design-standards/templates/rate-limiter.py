# Grey Haven Studio - Rate Limiter Template
# Add this to app/core/rate_limit.py

from fastapi import Request, HTTPException, status
from upstash_redis import Redis
import os

# Doppler provides REDIS_URL
redis = Redis.from_url(os.getenv("REDIS_URL"))


class RateLimiter:
    """
    Rate limiter using Upstash Redis.

    Usage:
        rate_limit_strict = RateLimiter(max_requests=10, window=60)
        rate_limit_normal = RateLimiter(max_requests=100, window=60)

        @router.post("", dependencies=[Depends(rate_limit_strict)])
        async def create_resource():
            pass
    """

    def __init__(self, max_requests: int = 100, window: int = 60):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum requests allowed in window
            window: Time window in seconds
        """
        self.max_requests = max_requests
        self.window = window

    async def __call__(self, request: Request):
        """Check rate limit for current request."""
        # Get client identifier (IP address or user ID from JWT)
        client_id = self._get_client_id(request)

        # Rate limit key
        key = f"rate_limit:{client_id}:{request.url.path}"

        # Increment counter
        count = redis.incr(key)

        # Set expiration on first request
        if count == 1:
            redis.expire(key, self.window)

        # Check if limit exceeded
        if count > self.max_requests:
            retry_after = redis.ttl(key)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again in {retry_after} seconds.",
                headers={"Retry-After": str(retry_after)},
            )

    def _get_client_id(self, request: Request) -> str:
        """Get client identifier (IP or user ID)."""
        # Prefer user ID from JWT if available
        if hasattr(request.state, "user") and request.state.user:
            return f"user:{request.state.user.id}"

        # Fallback to IP address
        return f"ip:{request.client.host}"


# Rate limit configurations
rate_limit_strict = RateLimiter(max_requests=10, window=60)  # 10 req/min
rate_limit_normal = RateLimiter(max_requests=100, window=60)  # 100 req/min
rate_limit_relaxed = RateLimiter(max_requests=1000, window=60)  # 1000 req/min


# Apply to routes:
# from app.core.rate_limit import rate_limit_strict, rate_limit_normal
#
# @router.post("", dependencies=[Depends(rate_limit_strict)])
# async def create_user():
#     """Create user (10 req/min limit)."""
#     pass
