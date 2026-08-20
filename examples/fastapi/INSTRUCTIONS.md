# Installation Instructions

This folder contains all the modules needed to fix the `ModuleNotFoundError` in your FastAPI application.

## What's Inside

```
fastapi_structure_fix/
├── __init__.py
├── auth/                          # Authentication module
│   ├── __init__.py
│   └── routes.py                 # Login/Register endpoints
├── middleware/                    # Middleware module
│   ├── __init__.py
│   └── auth_middleware.py         # JWT verification
├── rbac/                          # Role-Based Access Control
│   ├── __init__.py
│   ├── roles.py                  # Role definitions
│   └── authorization.py          # Permission checking
├── api/                           # API utilities
│   ├── __init__.py
│   ├── response_handler/
│   │   ├── __init__.py
│   │   └── response_formatter.py  # Response formatting
│   ├── pagination/
│   │   ├── __init__.py
│   │   └── paginator.py          # Pagination logic
│   ├── error_handling/
│   │   ├── __init__.py
│   │   └── fastapi_error_handler.py
│   └── logging/
│       ├── __init__.py
│       └── logger_config.py
└── security/                      # Security module
    ├── __init__.py
    ├── cors/
    │   ├── __init__.py
    │   └── cors_config.py        # CORS configuration
    └── rate_limit/
        ├── __init__.py
        └── fastapi_rate_limiter.py
```

## How to Add to Your Repo

### Option A: Copy via Git/GitHub (Recommended)

1. **Clone/Download these files** to your computer
2. **Copy the entire folder structure** into `examples/fastapi/`

Your final structure should look like:
```
examples/fastapi/
├── __init__.py
├── main.py
├── auth/
├── middleware/
├── rbac/
├── api/
├── security/
└── (pycache folders if you ran it)
```

3. **Commit and push to GitHub:**
```bash
cd your-repo-root
git add examples/fastapi/
git commit -m "Add missing modules to fix FastAPI import errors"
git push origin main
```

### Option B: Manual Copy (if you prefer)

1. Create each folder in `examples/fastapi/`:
   - `auth/`
   - `middleware/`
   - `rbac/`
   - `api/response_handler/`
   - `api/pagination/`
   - `api/error_handling/`
   - `api/logging/`
   - `security/cors/`
   - `security/rate_limit/`

2. Create `__init__.py` in each folder (can be empty)

3. Copy each `.py` file from the provided structure

## After Installation

### Install Dependencies

Your `requirements.fastapi.txt` should include:
```
fastapi==0.104.0
uvicorn[standard]==0.24.0
pydantic==2.4.0
pyjwt==2.8.0
python-multipart==0.0.6
python-dotenv==1.0.0
```

Install them:
```bash
pip install -r requirements.fastapi.txt
```

### Run the App

From your project root:
```bash
# Windows
set PYTHONPATH=%cd%
python -m uvicorn examples.fastapi.main:app --reload

# Mac/Linux
export PYTHONPATH=$(pwd)
python -m uvicorn examples.fastapi.main:app --reload
```

Or from the examples/fastapi folder:
```bash
cd examples/fastapi
python -m uvicorn main:app --reload
```

### Test the Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# Login (returns JWT token)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# Protected endpoint (replace TOKEN with your JWT)
curl http://localhost:8000/api/protected \
  -H "Authorization: Bearer TOKEN"

# Public endpoint
curl http://localhost:8000/api/public

# Get projects (requires auth + permission)
curl http://localhost:8000/api/projects \
  -H "Authorization: Bearer TOKEN"
```

## Troubleshooting

### Still getting `ModuleNotFoundError`?

**Make sure you're running from project root:**
```bash
# ✅ Correct - from project root
python -m uvicorn examples.fastapi.main:app --reload

# ❌ Wrong - from examples/fastapi folder
cd examples/fastapi && uvicorn main:app --reload
```

**Verify PYTHONPATH:**
```bash
# Before running, set this:
# Windows
set PYTHONPATH=%cd%

# Mac/Linux
export PYTHONPATH=$(pwd)
```

**Check file structure:**
Make sure all `__init__.py` files exist in each folder. They can be empty.

## Features Included

✅ JWT Authentication (Login/Register)
✅ Role-Based Access Control (RBAC)
✅ Permission checking
✅ CORS configuration
✅ Rate limiting setup
✅ Error handling
✅ Response formatting
✅ Pagination utilities
✅ Logging setup

## Next Steps

1. Add these files to your repo
2. Install dependencies
3. Test the endpoints
4. Update your React frontend to use the API endpoints
5. Customize users, permissions, and roles in `auth/routes.py`

## Need Help?

If you still have issues:
1. Check that all `__init__.py` files are present
2. Verify PYTHONPATH is set correctly
3. Make sure JWT_SECRET_KEY is set (defaults to a test key)
4. Check that all imports match your folder structure
