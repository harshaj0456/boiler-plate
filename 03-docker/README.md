# Docker Configuration

Production-ready Docker setup with multi-stage builds, non-root users, and health checks.

## Features

- Multi-stage builds (smaller images)
- Non-root user for security
- Production dependencies only
- Health checks
- Docker Compose for local development
- Environment variable configuration

## Quick Start

### FastAPI Stack
```bash
# Development
docker-compose -f docker-compose.fastapi.yml up --build

# Production
docker-compose -f docker-compose.fastapi.yml -f docker-compose.prod.yml up -d
```

### Flask Stack
```bash
# Development
docker-compose -f docker-compose.flask.yml up --build

# Production
docker-compose -f docker-compose.flask.yml -f docker-compose.prod.yml up -d
```

## Environment Variables

Create a `.env` file in the root directory:

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=app_db

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-in-production

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# API URL (for frontend)
VITE_API_URL=http://localhost:8000
```

## Docker Images

### Backend (FastAPI/Flask)
- Base: `python:3.11-slim`
- Multi-stage build
- Non-root user (uid: 1000)
- Health check on `/health` endpoint

### Frontend (React)
- Build: `node:20-alpine`
- Serve: `nginx:alpine`
- Non-root user
- Health check on root endpoint

### Database
- Image: `postgres:15-alpine`
- Persistent volume
- Health check with pg_isready

## Best Practices

1. **Multi-stage builds**: Reduces image size by ~60%
2. **Non-root user**: Security best practice
3. **.dockerignore**: Excludes unnecessary files
4. **Health checks**: Auto-recovery and monitoring
5. **Environment variables**: Configuration without code changes
6. **Production dependencies only**: Smaller, faster images

## Dockerfile Structure

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder
# Install dependencies

# Stage 2: Production
FROM python:3.11-slim
# Copy only necessary files
# Run as non-root user
```

## Commands

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (caution: deletes data)
docker-compose down -v
```
