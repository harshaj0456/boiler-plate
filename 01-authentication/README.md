# Authentication Module

Python-native authentication for FastAPI and Flask with JWT tokens.

## Features

- JWT access tokens (15 min expiry)
- Refresh tokens (7 days expiry)
- Password hashing with bcrypt
- User registration & login
- Token refresh endpoint
- Protected route decorators

## Request Flow

```
Request
  ↓
Authentication Middleware
  ↓
Verify JWT Token
  ↓
Extract User Info
  ↓
Proceed to Route
```

## Usage

### FastAPI
```python
from auth.jwt_auth import create_access_token, verify_token
from middleware.auth_middleware import require_auth

@app.post("/login")
async def login(credentials: LoginSchema):
    # ... validate user
    token = create_access_token(user_id=user.id)
    return {"access_token": token}

@app.get("/protected")
@require_auth
async def protected_route(current_user: dict):
    return {"user": current_user}
```

### Flask
```python
from auth.jwt_auth import create_access_token
from middleware.auth_middleware import require_auth

@app.route("/login", methods=["POST"])
def login():
    # ... validate user
    token = create_access_token(user_id=user.id)
    return {"access_token": token}

@app.route("/protected")
@require_auth
def protected_route(current_user):
    return {"user": current_user}
```
