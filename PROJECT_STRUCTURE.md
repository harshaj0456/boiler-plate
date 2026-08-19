# Project Structure

```
python-react-boilerplate/
│
├── 01-authentication/              # JWT-based authentication
│   ├── fastapi/
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── jwt_auth.py        # JWT token generation/validation
│   │   │   ├── models.py          # Pydantic models
│   │   │   └── routes.py          # Auth endpoints
│   │   └── middleware/
│   │       ├── __init__.py
│   │       └── auth_middleware.py # Authentication dependencies
│   │
│   ├── flask/
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── jwt_auth.py        # JWT utilities
│   │   │   └── routes.py          # Auth blueprint
│   │   └── middleware/
│   │       ├── __init__.py
│   │       └── auth_middleware.py # Auth decorators
│   │
│   └── README.md
│
├── 02-rbac/                        # Role-Based Access Control
│   ├── fastapi/
│   │   ├── __init__.py
│   │   ├── roles.py               # Role definitions
│   │   ├── permissions.py         # Permission constants
│   │   └── authorization.py       # Permission checking
│   │
│   ├── flask/
│   │   ├── __init__.py
│   │   ├── roles.py
│   │   ├── permissions.py
│   │   └── authorization.py       # Decorators
│   │
│   └── README.md
│
├── 03-docker/                      # Docker configurations
│   ├── fastapi/
│   │   ├── Dockerfile             # Multi-stage build
│   │   └── .dockerignore
│   │
│   ├── flask/
│   │   ├── Dockerfile
│   │   └── .dockerignore
│   │
│   ├── frontend/
│   │   ├── Dockerfile             # React + Nginx
│   │   ├── .dockerignore
│   │   └── nginx.conf             # Nginx configuration
│   │
│   ├── docker-compose.fastapi.yml # Full stack with FastAPI
│   ├── docker-compose.flask.yml   # Full stack with Flask
│   └── README.md
│
├── 04-jenkins/                     # CI/CD pipelines
│   ├── fastapi/
│   │   └── Jenkinsfile            # FastAPI pipeline
│   │
│   ├── flask/
│   │   └── Jenkinsfile            # Flask pipeline
│   │
│   └── README.md
│
├── 05-deployment/                  # Deployment guides
│   ├── aws/
│   │   ├── fastapi/
│   │   │   └── setup.sh           # EC2 setup script
│   │   │
│   │   ├── flask/
│   │   │   └── setup.sh
│   │   │
│   │   ├── nginx/
│   │   │   └── nginx.conf         # ALB -> EC2 config
│   │   │
│   │   └── README.md              # AWS deployment guide
│   │
│   └── vercel/
│       ├── vercel.json            # Vercel configuration
│       └── README.md              # Vercel deployment
│
├── 06-api/                         # API utilities
│   ├── error-handling/
│   │   ├── __init__.py
│   │   ├── fastapi_error_handler.py
│   │   └── flask_error_handler.py
│   │
│   ├── logging/
│   │   ├── __init__.py
│   │   └── logger_config.py       # Structured logging
│   │
│   ├── pagination/
│   │   ├── __init__.py
│   │   └── paginator.py           # Pagination utilities
│   │
│   ├── response-handler/
│   │   ├── __init__.py
│   │   └── response_formatter.py  # Standard responses
│   │
│   └── README.md
│
├── 07-security/                    # Security middleware
│   ├── cors/
│   │   ├── __init__.py
│   │   └── cors_config.py         # CORS configurations
│   │
│   ├── rate-limit/
│   │   ├── __init__.py
│   │   ├── fastapi_rate_limiter.py
│   │   └── flask_rate_limiter.py
│   │
│   └── README.md
│
├── examples/                       # Complete example apps
│   ├── fastapi/
│   │   └── main.py                # Full FastAPI example
│   │
│   ├── flask/
│   │   └── app.py                 # Full Flask example
│   │
│   └── README.md
│
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── requirements.fastapi.txt        # FastAPI dependencies
├── requirements.flask.txt          # Flask dependencies
├── README.md                       # Main documentation
├── QUICKSTART.md                   # Quick start guide
├── ARCHITECTURE.md                 # Architecture documentation
├── CONTRIBUTING.md                 # Contribution guidelines
└── PROJECT_STRUCTURE.md           # This file
```

## Module Descriptions

### 01-authentication
Python-native JWT authentication with access and refresh tokens. No external auth service needed.

**Key Files:**
- `jwt_auth.py` - Token generation, validation, password hashing
- `routes.py` - `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/me`
- `auth_middleware.py` - Dependency/decorator for protected routes

### 02-rbac
Role-based access control independent of authentication provider.

**Key Files:**
- `roles.py` - Role definitions (ADMIN, MANAGER, FIELD_WORKER, VOLUNTEER)
- `permissions.py` - Permission constants (resource.action pattern)
- `authorization.py` - Permission checking logic

**Roles Hierarchy:**
```
ADMIN (all permissions)
  └── MANAGER (project.*, beneficiary.*, donation.read)
      └── FIELD_WORKER (beneficiary.read/update, task.read/update)
          └── VOLUNTEER (project.read, task.update)
```

### 03-docker
Production-ready Docker configurations with multi-stage builds.

**Features:**
- Multi-stage builds (smaller images)
- Non-root users
- Health checks
- Docker Compose for local development

### 04-jenkins
Complete CI/CD pipelines with linting, testing, building, and deployment.

**Pipeline Stages:**
1. Checkout code
2. Install dependencies
3. Lint (flake8)
4. Run tests (pytest)
5. Build Docker image
6. Push to registry
7. Deploy to EC2
8. Health check

### 05-deployment
Deployment configurations for AWS and Vercel.

**AWS:**
- EC2 setup scripts
- ALB configuration
- Nginx reverse proxy
- Auto-scaling ready

**Vercel:**
- React frontend deployment
- Edge CDN
- Automatic HTTPS

### 06-api
Reusable API utilities for consistent API development.

**Modules:**
- **Error Handling** - Custom exceptions, centralized error handling
- **Logging** - Structured logging with rotation
- **Pagination** - Consistent pagination across endpoints
- **Response Handler** - Standard API response format

### 07-security
Security middleware for production applications.

**Modules:**
- **CORS** - Cross-origin resource sharing configuration
- **Rate Limiting** - Request rate limiting (Redis-backed in production)

### examples
Complete working examples demonstrating all features integrated together.

## File Naming Conventions

- Python files: `snake_case.py`
- Configuration files: `lowercase.yml`, `lowercase.json`
- Documentation: `UPPERCASE.md` (main docs), `README.md` (module docs)
- Docker files: `Dockerfile`, `.dockerignore`

## Import Path Examples

### FastAPI
```python
# Authentication
from auth.jwt_auth import create_access_token, verify_token
from middleware.auth_middleware import get_current_user

# RBAC
from rbac.roles import Role
from rbac.permissions import Permission
from rbac.authorization import require_permission

# API Utilities
from api.response_handler.response_formatter import success_response
from api.pagination.paginator import paginate, PaginationParams
from api.logging.logger_config import setup_logger

# Security
from security.cors.cors_config import get_fastapi_cors_config
from security.rate_limit.fastapi_rate_limiter import setup_rate_limiting
```

### Flask
```python
# Authentication
from auth.jwt_auth import create_access_token
from middleware.auth_middleware import require_auth

# RBAC
from rbac.authorization import require_permission, require_role

# API Utilities
from api.error_handling.flask_error_handler import register_error_handlers
from api.pagination.paginator import paginate

# Security
from security.rate_limit.flask_rate_limiter import get_rate_limiter
```

## Quick Navigation

- **Setup**: See `QUICKSTART.md`
- **Architecture**: See `ARCHITECTURE.md`
- **Contributing**: See `CONTRIBUTING.md`
- **Authentication**: See `01-authentication/README.md`
- **RBAC**: See `02-rbac/README.md`
- **Docker**: See `03-docker/README.md`
- **CI/CD**: See `04-jenkins/README.md`
- **Deployment**: See `05-deployment/aws/README.md`
- **API Utilities**: See `06-api/README.md`
- **Security**: See `07-security/README.md`
