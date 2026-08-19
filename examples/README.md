# Example Applications

Complete example applications demonstrating all boilerplate features.

## FastAPI Example (`fastapi/main.py`)

Full-featured FastAPI application with:
- JWT authentication
- Role-based access control
- Pagination
- Rate limiting
- Error handling
- Structured logging
- CORS configuration

### Running

```bash
# Install dependencies
pip install -r requirements.fastapi.txt

# Set environment variables
cp .env.example .env

# Run application
cd examples/fastapi
python main.py

# Or with uvicorn
uvicorn main:app --reload
```

### Available Endpoints

```
GET  /health              - Health check (no auth)
POST /auth/register       - Register user
POST /auth/login          - Login user
POST /auth/refresh        - Refresh token
GET  /auth/me             - Get current user (auth required)

GET  /api/public          - Public endpoint (rate limited)
GET  /api/protected       - Protected endpoint (auth required)
GET  /api/projects        - Get projects (auth + permission required)
DELETE /api/projects/{id} - Delete project (auth + role required)
POST /api/beneficiaries   - Create beneficiary (auth + permission required)
```

## Flask Example (`flask/app.py`)

Full-featured Flask application with same features as FastAPI.

### Running

```bash
# Install dependencies
pip install -r requirements.flask.txt

# Set environment variables
cp .env.example .env

# Run application
cd examples/flask
python app.py

# Or with Flask CLI
export FLASK_APP=app.py
flask run
```

### Available Endpoints

Same as FastAPI example.

## Testing the Examples

### 1. Register a User

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123",
    "username": "admin"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'
```

Save the `access_token` from the response.

### 3. Access Protected Endpoint

```bash
curl -X GET http://localhost:8000/api/protected \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Test RBAC (will fail without proper role)

```bash
curl -X GET http://localhost:8000/api/projects \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

This will fail with 403 because the user doesn't have the `project.read` permission. To test properly, you need to:

1. Modify the mock database in `auth/routes.py` to assign roles
2. Or add a database and assign roles programmatically

### 5. Test Rate Limiting

```bash
# Run this multiple times quickly
for i in {1..10}; do
  curl -X POST http://localhost:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{
      "email": "admin@example.com",
      "password": "wrong_password"
    }'
done
```

After 5 attempts, you should see a 429 rate limit error.

### 6. Test Pagination

```bash
curl -X GET "http://localhost:8000/api/projects?page=1&page_size=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Integration with Database

To use with a real database:

1. Create SQLAlchemy models
2. Replace mock data with database queries
3. Add migration scripts with Alembic
4. Configure database URL in `.env`

Example:

```python
# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String)
    password = Column(String)
    role = Column(String, default="VOLUNTEER")

# In routes
from sqlalchemy.orm import Session
from database import get_db

@app.get("/api/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

## Adding New Features

### Add a New Protected Route

```python
@app.get("/api/my-feature")
@require_permission("feature.read")
async def my_feature(
    current_user: dict = Depends(get_current_user)
):
    # Your logic
    return success_response(data={"feature": "data"})
```

### Add a New Role

1. Edit `rbac/roles.py`
2. Edit `rbac/permissions.py`
3. Edit `rbac/authorization.py` to map role to permissions

### Add Custom Middleware

```python
@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    # Before request
    response = await call_next(request)
    # After request
    return response
```
