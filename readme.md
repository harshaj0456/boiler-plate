# Python-React Boilerplate 🚀

> A production-ready, hackathon-friendly boilerplate for rapid development with Python (FastAPI/Flask) backend and React frontend.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)

**Perfect for NGO hackathons, rapid prototyping, and production applications.**

## ✨ Features

| Category | Features |
|----------|----------|
| **Authentication** | JWT tokens, refresh tokens, password hashing (bcrypt), register/login/refresh endpoints |
| **Authorization** | Role-based access control (RBAC), permission system (resource.action), 4 default roles |
| **API Utilities** | Pagination, error handling, response formatting, structured logging |
| **Security** | CORS configuration, rate limiting, security headers, input validation |
| **Docker** | Multi-stage builds, non-root users, health checks, docker-compose ready |
| **CI/CD** | Jenkins pipeline, automated testing, linting, deployment automation |
| **Deployment** | AWS (EC2 + ALB), Vercel (frontend), production-ready configs |

## 🏗️ Architecture

```
                    INTERNET
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
    VERCEL                          AWS
    (CDN)                       (ALB + EC2)
        │                             │
        │                      ┌──────┴──────┐
        ▼                      ▼             ▼
   React Frontend        FastAPI/Flask  FastAPI/Flask
                              │             │
                              └──────┬──────┘
                                     │
                                PostgreSQL
```

## 🚀 Quick Start (5 minutes)

### Option 1: Full Stack with Docker (Recommended)

```bash
# Clone/copy this boilerplate
git clone https://github.com/your-username/python-react-boilerplate.git
cd python-react-boilerplate

# Create environment file
cp .env.example .env

# Edit .env - at minimum change JWT_SECRET_KEY
# Generate: python -c "import secrets; print(secrets.token_hex(32))"

# Start everything (PostgreSQL + Backend + Frontend)
docker-compose -f 03-docker/docker-compose.fastapi.yml up --build

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Backend Only

```bash
# Install dependencies
pip install -r requirements.fastapi.txt  # or requirements.flask.txt

# Setup environment
cp .env.example .env

# Run database (Docker)
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:15-alpine

# Run backend
uvicorn main:app --reload  # FastAPI
# or
flask run  # Flask
```

📖 **Full guide**: See [QUICKSTART.md](./QUICKSTART.md)

## 📁 Project Structure

```
python-react-boilerplate/
├── 01-authentication/       # JWT authentication (FastAPI & Flask)
├── 02-rbac/                # Role-based access control
├── 03-docker/              # Docker configs & compose files
├── 04-jenkins/             # CI/CD pipelines
├── 05-deployment/          # AWS & Vercel deployment
├── 06-api/                 # API utilities (pagination, logging, etc.)
├── 07-security/            # CORS, rate limiting
├── examples/               # Complete working examples
├── QUICKSTART.md           # Detailed setup guide
├── ARCHITECTURE.md         # System architecture docs
└── PROJECT_STRUCTURE.md    # Complete file structure
```

## 🎯 Use Cases

**Perfect for:**
- 🏆 NGO/Social Impact Hackathons
- ⚡ Rapid MVP Development
- 🏢 Small to Medium Business Applications
- 📚 Learning Modern Web Architecture
- 🔧 Template for Production Apps

**Example Projects:**
- Donation management systems
- Volunteer coordination platforms
- Beneficiary tracking systems
- Project management tools
- Community platforms

## 🛡️ RBAC System

```
Roles Hierarchy:

ADMIN
├── All permissions (*)
└── Can manage everything

MANAGER
├── project.* (all project operations)
├── beneficiary.* (all beneficiary operations)
└── donation.read

FIELD_WORKER
├── beneficiary.read
├── beneficiary.update
└── task.update

VOLUNTEER
├── project.read
└── task.update
```

**Easily customizable** - Edit `02-rbac/roles.py` and `02-rbac/permissions.py`

## 🔥 Tech Stack

### Backend Options
- **FastAPI** (recommended) - Modern, async, auto-docs
- **Flask** - Classic, stable, well-documented

### Frontend
- **React** with Vite
- Deployed on Vercel CDN

### Database
- **PostgreSQL** 15+
- Docker-ready
- Migration support (Alembic/Flask-Migrate)

### Deployment
- **Backend**: AWS EC2 + Application Load Balancer
- **Frontend**: Vercel (automatic HTTPS, CDN)
- **CI/CD**: Jenkins
- **Container**: Docker with multi-stage builds

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](./QUICKSTART.md) | Get started in 5 minutes |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | System design & patterns |
| [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) | Complete file structure |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | How to contribute |
| [TODO.md](./TODO.md) | Planned features |

### Module Documentation
- [Authentication](./01-authentication/README.md) - JWT auth setup
- [RBAC](./02-rbac/README.md) - Role & permission system
- [Docker](./03-docker/README.md) - Container setup
- [Jenkins](./04-jenkins/README.md) - CI/CD pipeline
- [Deployment](./05-deployment/README.md) - AWS & Vercel
- [API Utilities](./06-api/README.md) - Reusable utilities
- [Security](./07-security/README.md) - Security configs

## 💻 Example API Usage

### Register & Login
```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass123","username":"user"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass123"}'
```

### Protected Endpoint
```bash
curl -X GET http://localhost:8000/api/protected \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### With RBAC
```python
@app.delete("/projects/{project_id}")
async def delete_project(
    project_id: int,
    current_user: dict = Depends(get_current_user),
    _: None = Depends(require_permission("project.delete"))
):
    # Only users with project.delete permission can access
    return {"message": "Deleted"}
```

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v --cov

# Run linting
flake8 .
black . --check
```

## 🌐 Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

### Backend (AWS EC2)
```bash
# Automated via Jenkins pipeline
# Or manually:
ssh ubuntu@your-ec2-ip
git pull
docker-compose up -d --build
```

See [05-deployment/](./05-deployment/) for detailed guides.

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for hackathons and rapid prototyping
- Designed with NGO/social impact projects in mind
- Community-driven development

## 📞 Support

- 📖 Documentation: Read the docs in each module
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/python-react-boilerplate/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/your-username/python-react-boilerplate/discussions)

## ⭐ Star Us!

If this boilerplate helped you, please give it a star on GitHub! It helps others discover the project.

---

**Built with ❤️ for developers who move fast and build things that matter.**


## Hackathon Frontend

The repository now includes a generic React + Vite + Tailwind frontend in `frontend/`.

### Frontend stack
- React + Vite
- Tailwind CSS v4
- React Router
- Axios + TanStack Query
- React Hook Form + Zod-ready utilities
- Lucide icons
- Framer Motion
- Recharts
- Swiper
- Sonner toasts
- PWA support via `vite-plugin-pwa`

### Run locally
```bash
cd frontend
npm install
npm run dev
```
Frontend: http://localhost:5173
Backend (FastAPI): http://localhost:8000
API docs: http://localhost:8000/docs

Create `frontend/.env` from `frontend/.env.example`:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Hackathon App
```

The frontend is domain-agnostic and should be customized per problem statement.
