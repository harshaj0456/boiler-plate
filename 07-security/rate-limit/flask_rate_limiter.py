from flask import request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os


def get_rate_limiter():
    """
    Initialize and return Flask-Limiter instance.
    
    Usage:
        from flask import Flask
        from rate_limiter import get_rate_limiter
        
        app = Flask(__name__)
        limiter = get_rate_limiter()
        limiter.init_app(app)
    """
    return Limiter(
        key_func=get_remote_address,
        default_limits=["100 per minute"],
        storage_uri=os.getenv("REDIS_URL", "memory://"),  # Use Redis in production
        storage_options={},
    )


def rate_limit_error_handler(e):
    """Custom rate limit error handler."""
    return jsonify({
        "error": "Rate limit exceeded",
        "message": "Too many requests. Please try again later.",
        "retry_after": e.description
    }), 429


# Example usage:
"""
from flask import Flask
from rate_limiter import get_rate_limiter, rate_limit_error_handler

app = Flask(__name__)
limiter = get_rate_limiter()
limiter.init_app(app)

# Register error handler
@app.errorhandler(429)
def handle_rate_limit(e):
    return rate_limit_error_handler(e)

# Apply to specific routes
@app.route("/api/endpoint")
@limiter.limit("10 per minute")
def endpoint():
    return {"message": "Success"}

# Auth endpoints
@app.route("/auth/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    return {"message": "Login successful"}

# Exempt certain routes
@app.route("/health")
@limiter.exempt
def health():
    return {"status": "healthy"}
"""


# Common decorators
def strict_limit(limiter):
    """Strict rate limit: 10 requests per minute."""
    return limiter.limit("10 per minute")


def moderate_limit(limiter):
    """Moderate rate limit: 50 requests per minute."""
    return limiter.limit("50 per minute")


def relaxed_limit(limiter):
    """Relaxed rate limit: 200 requests per minute."""
    return limiter.limit("200 per minute")


def auth_limit(limiter):
    """Rate limit for authentication: 5 attempts per minute."""
    return limiter.limit("5 per minute")
