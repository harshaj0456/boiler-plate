from typing import List
import os


# FastAPI CORS Configuration
def get_fastapi_cors_config():
    """
    Get CORS configuration for FastAPI.
    
    Usage:
        from fastapi.middleware.cors import CORSMiddleware
        from cors_config import get_fastapi_cors_config
        
        app = FastAPI()
        config = get_fastapi_cors_config()
        app.add_middleware(CORSMiddleware, **config)
    """
    allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    return {
        "allow_origins": allowed_origins,
        "allow_credentials": True,
        "allow_methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        "allow_headers": [
            "Authorization",
            "Content-Type",
            "Accept",
            "Origin",
            "User-Agent",
            "DNT",
            "Cache-Control",
            "X-Requested-With",
        ],
        "expose_headers": [
            "Content-Length",
            "Content-Range",
            "X-Total-Count",
        ],
        "max_age": 600,  # Cache preflight requests for 10 minutes
    }


# Flask CORS Configuration
def get_flask_cors_config():
    """
    Get CORS configuration for Flask.
    
    Usage:
        from flask_cors import CORS
        from cors_config import get_flask_cors_config
        
        app = Flask(__name__)
        CORS(app, **get_flask_cors_config())
    """
    allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    return {
        "origins": allowed_origins,
        "supports_credentials": True,
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        "allow_headers": [
            "Authorization",
            "Content-Type",
            "Accept",
            "Origin",
            "User-Agent",
            "DNT",
            "Cache-Control",
            "X-Requested-With",
        ],
        "expose_headers": [
            "Content-Length",
            "Content-Range",
            "X-Total-Count",
        ],
        "max_age": 600,
    }


# Strict CORS for Production
def get_production_cors_config(allowed_origins: List[str]):
    """
    Strict CORS configuration for production.
    Only allows specified origins.
    """
    return {
        "allow_origins": allowed_origins,
        "allow_credentials": True,
        "allow_methods": ["GET", "POST", "PUT", "DELETE"],  # No PATCH in strict mode
        "allow_headers": ["Authorization", "Content-Type"],
        "max_age": 3600,
    }
