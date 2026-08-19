# Architecture Documentation

## Overview

This boilerplate implements a modern, production-ready architecture for Python-React applications with authentication, authorization, and deployment configurations.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         INTERNET                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                  │
        ▼                                  ▼
   ┌─────────┐                       ┌──────────┐
   │ VERCEL  │                       │   AWS    │
   │ (CDN)   │                       │   ALB    │
   └────┬────┘                       └────┬─────┘
        │                                  │
        │                          ┌───────┴────────┐
        │                          │                │
        ▼                          ▼                ▼
   React Frontend              EC2 #1           EC2 #2
                               │                │
                            Docker           Docker
                               │                │
                          FastAPI/Flask    FastAPI/Flask
                               │                │
                               └────────┬───────┘
                                        │
                                   PostgreSQL
```

## Request Flow

### Authentication Flow

```
1. User Registration/Login
   ↓
2. Credentials Validation
   ↓
3. Password Hashing (bcrypt)
   ↓
4. JWT Token Generation
   ↓
5. Return Access Token + Refresh Token
   ↓
6. Client stores tokens
   ↓
7. Subsequent requests include Access Token in header
   ↓
8. Backend validates JWT
   ↓
9. Extract user information
   ↓
10. Proceed to authorization
```

### Authorization Flow (RBAC)

```
Request with JWT Token
   ↓
Authentication Middleware
   ↓
Extract User Info (user_id, role)
   ↓
RBAC Middleware
   ↓
Check: Does user's role have required permission?
   ↓
   ├── YES → Proceed to Controller
   └── NO  → Return 403 Forbidden
```

## Component Architecture

### Backend Layers

```
┌───────────────────────────────────────────┐
│          API Layer (Routes)               │
│  - Define endpoints                       │
│  - Request/Response handling              │
└──────────────┬────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────┐
│       Middleware Layer                    │
│  - Authentication                         │
│  - Authorization (RBAC)                   │
│  - Rate Limiting                          │
│  - CORS                                   │
│  - Logging                                │
└──────────────┬────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────┐
│       Business Logic Layer                │
│  - Application logic                      │
│  - Data validation                        │
│  - Business rules                         │
└──────────────┬────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────┐
│       Data Access Layer                   │
│  - ORM (SQLAlchemy)                       │
│  - Database queries                       │
│  - Data models                            │
└──────────────┬────────────────────────────┘
               │
               ▼
         PostgreSQL Database
```

### Frontend Architecture

```
┌───────────────────────────────────────────┐
│          UI Components                    │
│  - React components                       │
│  - Pages                                  │
│  - Forms                                  │
└──────────────┬────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────┐
│       State Management                    │
│  - React Context / Redux                  │
│  - Local state                            │
└──────────────┬────────────────────────────┘
               │
               ▼
┌───────────────────────────────────────────┐
│       API Layer                           │
│  - Axios/Fetch                            │
│  - API client                             │
│  - Token management                       │
└──────────────┬────────────────────────────┘
               │
               ▼
         Backend API
```

## Security Architecture

### Defense in Depth

```
Layer 1: Network Security
├── ALB (AWS)
├── Security Groups
└── VPC

Layer 2: Application Security
├── CORS
├── Rate Limiting
├── Input Validation
└── Security Headers

Layer 3: Authentication & Authorization
├── JWT Tokens
├── Password Hashing
├── RBAC
└── Permission Checks

Layer 4: Data Security
├── SQL Injection Prevention (ORM)
├── XSS Prevention
└── CSRF Protection

Layer 5: Monitoring & Logging
├── Access Logs
├── Error Logs
└── Audit Logs
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,  -- bcrypt hashed
    role VARCHAR(50) NOT NULL,       -- ADMIN, MANAGER, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sessions Table (Optional - for refresh tokens)
```sql
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    refresh_token VARCHAR(500) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Deployment Architecture

### Development
```
Developer Machine
  ├── Backend: localhost:8000/5000
  ├── Frontend: localhost:3000
  └── Database: localhost:5432 (Docker)
```

### Staging
```
AWS Environment (Staging)
  ├── Backend: staging-api.yourdomain.com (EC2)
  ├── Frontend: staging.yourdomain.com (Vercel)
  └── Database: RDS (PostgreSQL)
```

### Production
```
AWS Environment (Production)
  ├── ALB: api.yourdomain.com
  ├── EC2 Auto Scaling Group (2-10 instances)
  ├── Frontend: yourdomain.com (Vercel CDN)
  ├── Database: RDS Multi-AZ (PostgreSQL)
  └── Cache: ElastiCache (Redis) - for rate limiting
```

## CI/CD Pipeline

```
Developer Commits Code
  ↓
GitHub Repository
  ↓
GitHub Webhook
  ↓
Jenkins Server
  ├── Checkout Code
  ├── Run Linters (flake8, black)
  ├── Run Tests (pytest)
  ├── Build Docker Image
  ├── Push to Registry
  ├── Deploy to EC2
  └── Health Check
  ↓
Deployed Application
```

## Scalability Considerations

### Horizontal Scaling
- Multiple EC2 instances behind ALB
- Stateless application design
- JWT tokens (no session storage)
- Shared database (RDS)

### Vertical Scaling
- Increase EC2 instance size
- Database read replicas
- Connection pooling

### Caching Strategy
```
Request
  ↓
Check Redis Cache
  ├── Hit: Return cached data
  └── Miss: Query database → Store in cache → Return
```

## Monitoring & Observability

### Metrics to Track
- Request latency
- Error rates
- Authentication success/failure
- Rate limit hits
- Database query performance
- CPU/Memory usage

### Logging Strategy
```
Application Logs
  ├── Info: Normal operations
  ├── Warning: Potential issues
  ├── Error: Failures
  └── Debug: Detailed debugging

Access Logs
  ├── All API requests
  └── Response times

Audit Logs
  ├── User logins
  ├── Permission changes
  └── Critical operations
```

## Performance Optimization

1. **Database**
   - Indexes on frequently queried fields
   - Connection pooling
   - Query optimization

2. **Application**
   - Async/await (FastAPI)
   - Caching (Redis)
   - Rate limiting

3. **Frontend**
   - Code splitting
   - Lazy loading
   - CDN (Vercel)
   - Asset optimization

4. **Infrastructure**
   - ALB health checks
   - Auto-scaling
   - Multi-AZ deployment

## Disaster Recovery

### Backup Strategy
- Daily database backups (RDS snapshots)
- Application logs to S3
- Configuration in version control

### Recovery Time Objective (RTO)
- Target: < 1 hour
- Multi-AZ RDS for automatic failover
- Multiple EC2 instances

### Recovery Point Objective (RPO)
- Target: < 15 minutes
- Frequent database backups
- Transaction logs
