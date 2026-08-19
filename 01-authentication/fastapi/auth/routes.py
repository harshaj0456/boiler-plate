from fastapi import APIRouter, HTTPException, status, Depends
from .models import (
    UserRegistrationSchema,
    UserLoginSchema,
    TokenResponse,
    RefreshTokenRequest,
    UserResponse
)
from .jwt_auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token
)
from ..middleware.auth_middleware import get_current_user
import jwt

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Mock database - replace with actual database
users_db = {}


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegistrationSchema):
    """Register a new user."""
    
    # Check if user already exists
    if user_data.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    
    # Store user (replace with actual database insertion)
    user_id = len(users_db) + 1
    users_db[user_data.email] = {
        "id": user_id,
        "email": user_data.email,
        "username": user_data.username,
        "password": hashed_password
    }
    
    # Create tokens
    access_token = create_access_token(user_id=user_id)
    refresh_token = create_refresh_token(user_id=user_id)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLoginSchema):
    """Login a user."""
    
    # Get user from database
    user = users_db.get(credentials.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create tokens
    access_token = create_access_token(user_id=user["id"])
    refresh_token = create_refresh_token(user_id=user["id"])
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token_data: RefreshTokenRequest):
    """Refresh an access token using a refresh token."""
    
    try:
        payload = verify_token(token_data.refresh_token, token_type="refresh")
        user_id = payload["user_id"]
        
        # Create new tokens
        access_token = create_access_token(user_id=user_id)
        refresh_token = create_refresh_token(user_id=user_id)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired"
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user information."""
    
    user_id = current_user["user_id"]
    
    # Find user by ID (replace with actual database query)
    user = next((u for u in users_db.values() if u["id"] == user_id), None)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=user["id"],
        email=user["email"],
        username=user["username"]
    )
