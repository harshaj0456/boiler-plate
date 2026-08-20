"""CORS configuration."""

import os

def get_fastapi_cors_config() -> dict:
    """
    Get CORS configuration for FastAPI.
    
    Returns:
        Dict with CORS settings for CORSMiddleware
    """
    allowed_origins = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:5173"
    ).split(",")
    
    return {
        "allow_origins": allowed_origins,
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
