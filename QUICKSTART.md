# Quick Start Guide

Get your Python-React application running in 5 minutes.

## Prerequisites

- Docker & Docker Compose
- Git
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

## Option 1: Full Stack with Docker (Recommended)

### FastAPI + React

```bash
# Clone or copy this boilerplate
cd python-react-boilerplate

# Create environment file
cp .env.example .env

# Edit .env with your values (at minimum, change JWT_SECRET_KEY)

# Start all services (PostgreSQL, FastAPI, React)
docker-compose -f 03-docker/docker-compose.fastapi.yml up --build

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Flask + React

```bash
# Same steps, but use Flask compose file
docker-compose -f 03-docker/docker-compose.flask.yml up --build

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
# API Docs: N/A (add Swagger if needed)
```

## Option 2: Backend Only (Local Development)

### FastAPI

```bash
# Install dependencies
pip install -r requirements.fastapi.txt

# Set environment variables
cp .env.example .env

# Run database (Docker)
docker run -d -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=app_db \
  postgres:15-alpine

# Run FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Flask

```bash
# Install dependencies
pip install -r requirements.flask.txt

# Set environment variables
cp .env.example .env

# Run database (Docker)
docker run -d -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=app_db \
  postgres:15-alpine

# Run Flask
flask run --host 0.0.0.0 --port 5000
```

## Option 3: Frontend Only

```bash
cd frontend

# Install dependencies
npm install

# Create .env
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Run development server
npm run dev

# Access: http://localhost:5173
```

## Testing the Setup

### Register a User

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "username": "testuser"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Access Protected Route

```bash
# Use the access_token from login response
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Project Structure Setup

Create your main application files:

### FastAPI (main.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as auth_router

app = FastAPI(title="My API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth_router)

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### Flask (app.py)

```python
from flask import Flask
from flask_cors import CORS
from auth.routes import auth_bp

app = Flask(__name__)
CORS(app)

# Routes
app.register_blueprint(auth_bp)

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

## Next Steps

1. **Customize RBAC**: Edit `02-rbac/` files to match your roles/permissions
2. **Add Database Models**: Create SQLAlchemy/SQLModel models
3. **Build Frontend**: Create React components in `frontend/src/`
4. **Setup CI/CD**: Configure Jenkins with your repository
5. **Deploy**: Follow `05-deployment/` guides

## Common Issues

### Port Already in Use
```bash
# Find and kill process
# Linux/Mac:
lsof -i :8000
kill -9 <PID>

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify network connectivity

### CORS Errors
- Check CORS_ORIGINS in .env
- Ensure frontend URL is whitelisted
- Check browser console for details

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Docker Documentation](https://docs.docker.com/)
