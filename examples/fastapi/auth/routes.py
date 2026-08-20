"""Authentication routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
import jwt
import os

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Mock users database (keyed by email now)
USERS_DB = {
    "admin@example.com": {
        "user_id": "admin",
        "username": "admin",
        "email": "admin@example.com",
        "password": "admin123",
        "name": "Admin User",
        "role": "admin",
        "permissions": ["project.read", "project.write", "project.delete", "beneficiary.create", "beneficiary.read"]
    },
    "user@example.com": {
        "user_id": "user1",
        "username": "user1",
        "email": "user@example.com",
        "password": "password123",
        "name": "Test User",
        "role": "user",
        "permissions": ["project.read", "beneficiary.read"]
    }
}

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    username: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "user"

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """User login endpoint."""
    user = USERS_DB.get(request.email)
    
    if not user or user["password"] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "user_id": user["user_id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
        "permissions": user["permissions"],
        "exp": expires
    }
    
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user_id=user["user_id"],
        username=user["username"]
    )

@router.post("/register", response_model=LoginResponse)
async def register(request: RegisterRequest):
    """User registration endpoint."""
    if request.email in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = {
        "user_id": request.email.split("@")[0],
        "username": request.email.split("@")[0],
        "email": request.email,
        "password": request.password,  # In production, hash this!
        "name": request.name,
        "role": request.role,
        "permissions": ["project.read", "beneficiary.read"]
    }
    
    USERS_DB[request.email] = new_user
    
    # Create access token
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "user_id": new_user["user_id"],
        "username": new_user["username"],
        "email": new_user["email"],
        "role": new_user["role"],
        "permissions": new_user["permissions"],
        "exp": expires
    }
    
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user_id=new_user["user_id"],
        username=new_user["username"]
    )

@router.get("/logout")
async def logout():
    """Logout endpoint (client should discard token)."""
    return {"message": "Logout successful"}