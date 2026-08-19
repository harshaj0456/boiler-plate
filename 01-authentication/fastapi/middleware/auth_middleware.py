from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt

from ..auth.jwt_auth import verify_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency to get the current authenticated user.
    
    Usage:
        @app.get("/protected")
        async def protected_route(current_user: dict = Depends(get_current_user)):
            return {"user_id": current_user["user_id"]}
    """
    token = credentials.credentials
    
    try:
        payload = verify_token(token, token_type="access")
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    )
) -> Optional[dict]:
    """
    Dependency to optionally get the current user.
    Returns None if no token is provided.
    
    Usage:
        @app.get("/public")
        async def public_route(current_user: Optional[dict] = Depends(get_optional_user)):
            if current_user:
                return {"message": f"Hello {current_user['user_id']}"}
            return {"message": "Hello guest"}
    """
    if not credentials:
        return None
    
    try:
        payload = verify_token(credentials.credentials, token_type="access")
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
