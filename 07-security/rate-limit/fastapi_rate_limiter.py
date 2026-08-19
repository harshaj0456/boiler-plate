from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import Callable
import os


# Initialize limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"],  # Default rate limit
    storage_uri=os.getenv("REDIS_URL", "memory://"),  # Use Redis in production
)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Custom rate limit exceeded handler."""
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": "Rate limit exceeded",
            "message": "Too many requests. Please try again later.",
            "retry_after": exc.detail
        }
    )


# Common rate limit decorators
def strict_rate_limit():
    """Strict rate limit: 10 requests per minute."""
    return limiter.limit("10/minute")


def moderate_rate_limit():
    """Moderate rate limit: 50 requests per minute."""
    return limiter.limit("50/minute")


def relaxed_rate_limit():
    """Relaxed rate limit: 200 requests per minute."""
    return limiter.limit("200/minute")


def auth_rate_limit():
    """Rate limit for authentication endpoints: 5 attempts per minute."""
    return limiter.limit("5/minute")


# Setup function
def setup_rate_limiting(app):
    """
    Setup rate limiting for FastAPI app.
    
    Usage:
        from fastapi import FastAPI
        from rate_limiter import setup_rate_limiting, limiter, strict_rate_limit
        
        app = FastAPI()
        setup_rate_limiting(app)
        
        @app.get("/api/endpoint")
        @strict_rate_limit()
        async def endpoint():
            return {"message": "Success"}
    """
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


# Example usage:
"""
from fastapi import FastAPI, Depends
from rate_limiter import setup_rate_limiting, limiter, auth_rate_limit

app = FastAPI()
setup_rate_limiting(app)

@app.post("/auth/login")
@auth_rate_limit()
async def login(request: Request):
    # Login logic
    return {"message": "Login successful"}

@app.get("/api/users")
@limiter.limit("50/minute")
async def get_users(request: Request):
    # Get users logic
    return {"users": []}
"""
