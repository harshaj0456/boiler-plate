from functools import wraps
from flask import request, jsonify
import jwt

from ..auth.jwt_auth import verify_token


def require_auth(f):
    """
    Decorator to require authentication on Flask routes.
    
    Usage:
        @app.route("/protected")
        @require_auth
        def protected_route(current_user):
            return {"user_id": current_user["user_id"]}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return jsonify({"error": "Missing authorization header"}), 401
        
        try:
            # Extract token from "Bearer <token>"
            scheme, token = auth_header.split()
            
            if scheme.lower() != "bearer":
                return jsonify({"error": "Invalid authentication scheme"}), 401
            
            # Verify token
            payload = verify_token(token, token_type="access")
            
            # Pass user info to route
            return f(current_user=payload, *args, **kwargs)
        
        except ValueError:
            return jsonify({"error": "Invalid authorization header format"}), 401
        
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
    
    return decorated_function


def optional_auth(f):
    """
    Decorator to optionally extract user info if token is present.
    
    Usage:
        @app.route("/public")
        @optional_auth
        def public_route(current_user=None):
            if current_user:
                return {"message": f"Hello {current_user['user_id']}"}
            return {"message": "Hello guest"}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return f(current_user=None, *args, **kwargs)
        
        try:
            scheme, token = auth_header.split()
            
            if scheme.lower() != "bearer":
                return f(current_user=None, *args, **kwargs)
            
            payload = verify_token(token, token_type="access")
            return f(current_user=payload, *args, **kwargs)
        
        except (ValueError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return f(current_user=None, *args, **kwargs)
    
    return decorated_function
