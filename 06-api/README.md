# API Utilities

Reusable API utilities for consistent API development.

## Modules

### 1. Response Handler
Standardized API response format.

```python
from response_handler.response_formatter import success_response, error_response

# Success response
return success_response(data=user, message="User retrieved")

# Error response
return error_response(message="User not found", details={"user_id": 123})
```

**Response Format:**
```json
{
  "success": true,
  "data": {...},
  "message": "Success",
  "timestamp": "2024-01-01T00:00:00"
}
```

### 2. Pagination
Consistent pagination across all endpoints.

```python
from pagination.paginator import paginate, PaginationParams

# Get pagination params from request
params = PaginationParams(page=1, page_size=20)

# Paginate results
result = paginate(items, total=100, page=1, page_size=20)
```

**Pagination Response:**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5,
  "has_next": true,
  "has_prev": false
}
```

### 3. Error Handling
Centralized error handling with custom exceptions.

**FastAPI:**
```python
from error_handling.fastapi_error_handler import (
    NotFoundException,
    UnauthorizedException,
    register_exception_handlers
)

app = FastAPI()
register_exception_handlers(app)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = get_user_from_db(user_id)
    if not user:
        raise NotFoundException(message="User not found")
    return user
```

**Flask:**
```python
from error_handling.flask_error_handler import (
    NotFoundException,
    register_error_handlers
)

app = Flask(__name__)
register_error_handlers(app)

@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = get_user_from_db(user_id)
    if not user:
        raise NotFoundException(message="User not found")
    return jsonify(user)
```

### 4. Logging
Structured logging with rotation.

```python
from logging.logger_config import setup_logger

# Setup logger
logger = setup_logger(name="my_app", level="INFO")

# Use logger
logger.info("Application started")
logger.error("An error occurred", extra={"user_id": 123})

# JSON logging for production
logger = setup_logger(name="my_app", json_format=True)
```

## Complete Example

### FastAPI
```python
from fastapi import FastAPI, Depends
from pagination.paginator import paginate, PaginationParams
from response_handler.response_formatter import success_response
from error_handling.fastapi_error_handler import (
    NotFoundException,
    register_exception_handlers
)
from logging.logger_config import setup_logger

app = FastAPI()
register_exception_handlers(app)
logger = setup_logger("api")

@app.get("/users")
async def get_users(pagination: PaginationParams = Depends()):
    logger.info(f"Fetching users: page={pagination.page}")
    
    # Get users from database
    users, total = get_users_from_db(
        offset=pagination.get_offset(),
        limit=pagination.get_limit()
    )
    
    # Paginate response
    result = paginate(users, total, pagination.page, pagination.page_size)
    
    return success_response(data=result, message="Users retrieved")

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = get_user_from_db(user_id)
    
    if not user:
        raise NotFoundException(message="User not found")
    
    return success_response(data=user, message="User retrieved")
```

### Flask
```python
from flask import Flask, request, jsonify
from pagination.paginator import paginate, PaginationParams
from response_handler.response_formatter import success_response
from error_handling.flask_error_handler import (
    NotFoundException,
    register_error_handlers
)
from logging.logger_config import setup_logger

app = Flask(__name__)
register_error_handlers(app)
logger = setup_logger("api")

@app.route("/users")
def get_users():
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 20, type=int)
    
    logger.info(f"Fetching users: page={page}")
    
    # Get users from database
    users, total = get_users_from_db(
        offset=(page - 1) * page_size,
        limit=page_size
    )
    
    # Paginate response
    result = paginate(users, total, page, page_size)
    
    return jsonify(success_response(data=result, message="Users retrieved"))

@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = get_user_from_db(user_id)
    
    if not user:
        raise NotFoundException(message="User not found")
    
    return jsonify(success_response(data=user, message="User retrieved"))
```
