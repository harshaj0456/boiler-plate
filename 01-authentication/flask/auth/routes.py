from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError, validates
import jwt

from .jwt_auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token
)
from ..middleware.auth_middleware import require_auth

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Mock database - replace with actual database
users_db = {}


# Schemas
class UserRegistrationSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    username = fields.Str(required=True)
    
    @validates("password")
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long")


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class RefreshTokenSchema(Schema):
    refresh_token = fields.Str(required=True)


# Routes
@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user."""
    
    schema = UserRegistrationSchema()
    
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    # Check if user already exists
    if data["email"] in users_db:
        return jsonify({"error": "Email already registered"}), 400
    
    # Hash password
    hashed_password = hash_password(data["password"])
    
    # Store user (replace with actual database insertion)
    user_id = len(users_db) + 1
    users_db[data["email"]] = {
        "id": user_id,
        "email": data["email"],
        "username": data["username"],
        "password": hashed_password
    }
    
    # Create tokens
    access_token = create_access_token(user_id=user_id)
    refresh_token = create_refresh_token(user_id=user_id)
    
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Login a user."""
    
    schema = UserLoginSchema()
    
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    # Get user from database
    user = users_db.get(data["email"])
    
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Verify password
    if not verify_password(data["password"], user["password"]):
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Create tokens
    access_token = create_access_token(user_id=user["id"])
    refresh_token = create_refresh_token(user_id=user["id"])
    
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    })


@auth_bp.route("/refresh", methods=["POST"])
def refresh_token_route():
    """Refresh an access token using a refresh token."""
    
    schema = RefreshTokenSchema()
    
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    try:
        payload = verify_token(data["refresh_token"], token_type="refresh")
        user_id = payload["user_id"]
        
        # Create new tokens
        access_token = create_access_token(user_id=user_id)
        refresh_token = create_refresh_token(user_id=user_id)
        
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        })
    
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token has expired"}), 401
    
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid refresh token"}), 401


@auth_bp.route("/me", methods=["GET"])
@require_auth
def get_me(current_user):
    """Get current user information."""
    
    user_id = current_user["user_id"]
    
    # Find user by ID (replace with actual database query)
    user = next((u for u in users_db.values() if u["id"] == user_id), None)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "id": user["id"],
        "email": user["email"],
        "username": user["username"]
    })
