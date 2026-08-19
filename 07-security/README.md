# Security Module

Security middleware and configurations for production-ready applications.

## Features

- CORS configuration
- Rate limiting
- Security headers
- Input validation
- SQL injection prevention

## CORS (Cross-Origin Resource Sharing)

### FastAPI
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cors.cors_config import get_fastapi_cors_config

app = FastAPI()

# Apply CORS
config = get_fastapi_cors_config()
app.add_middleware(CORSMiddleware, **config)
```

### Flask
```python
from flask import Flask
from flask_cors import CORS
from cors.cors_config import get_flask_cors_config

app = Flask(__name__)

# Apply CORS
CORS(app, **get_flask_cors_config())
```

## Rate Limiting

### FastAPI with Slowapi
```python
from rate_limit.fastapi_rate_limiter import setup_rate_limiting, auth_rate_limit

app = FastAPI()
setup_rate_limiting(app)

@app.post("/auth/login")
@auth_rate_limit()
async def login():
    return {"message": "Login successful"}
```

### Flask with Flask-Limiter
```python
from rate_limit.flask_rate_limiter import get_rate_limiter

app = Flask(__name__)
limiter = get_rate_limiter()
limiter.init_app(app)

@app.route("/auth/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    return {"message": "Login successful"}
```

## Environment Variables

```env
# CORS
CORS_ORIGINS=https://frontend.com,https://www.frontend.com

# Rate Limiting (use Redis in production)
REDIS_URL=redis://localhost:6379
```

## Production Recommendations

1. **Always use HTTPS** in production
2. **Use Redis** for rate limiting in production (not in-memory)
3. **Whitelist specific origins** instead of using wildcards
4. **Set strict rate limits** for authentication endpoints
5. **Monitor rate limit metrics** to detect attacks

## Security Headers

Add these headers in your nginx/ALB configuration:
```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

## Input Validation

Always validate user input:
- Use Pydantic (FastAPI) or Marshmallow (Flask)
- Sanitize database queries (use ORMs)
- Validate file uploads
- Check content types
