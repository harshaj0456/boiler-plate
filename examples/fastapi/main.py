"""
FastAPI Complete Example Application
Demonstrates all boilerplate features integrated together.
"""

# ADD THIS PATH FIX AT THE VERY TOP
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
# END OF PATH FIX

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Authentication
from auth.routes import router as auth_router
from middleware.auth_middleware import get_current_user

# RBAC
from rbac.authorization import require_permission, require_role
from rbac.roles import Role

# API Utilities
from api.response_handler.response_formatter import success_response
from api.pagination.paginator import PaginationParams, paginate
from api.error_handling.fastapi_error_handler import register_exception_handlers
from api.logging.logger_config import setup_logger

# Security
from security.cors.cors_config import get_fastapi_cors_config
from security.rate_limit.fastapi_rate_limiter import setup_rate_limiting, limiter, auth_rate_limit


# Setup logger
logger = setup_logger(name="fastapi_app", level="INFO")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("Application starting...")
    yield
    logger.info("Application shutting down...")


# Create app
app = FastAPI(
    title="Python-React Boilerplate API",
    description="Production-ready FastAPI boilerplate",
    version="1.0.0",
    lifespan=lifespan
)

# Setup middlewares
app.add_middleware(CORSMiddleware, **get_fastapi_cors_config())
setup_rate_limiting(app)

# Register exception handlers
register_exception_handlers(app)

# Include routers
app.include_router(auth_router)


# Health check (no auth, no rate limit)
@app.get("/health")
async def health():
    """Health check endpoint for load balancers."""
    return {"status": "healthy", "version": "1.0.0"}


# Public endpoint with rate limit
@app.get("/api/public")
@limiter.limit("100/minute")
async def public_endpoint(request: Request):
    """Public endpoint with rate limiting."""
    logger.info("Public endpoint accessed")
    return success_response(
        data={"message": "This is a public endpoint"},
        message="Success"
    )


# Protected endpoint (requires authentication)
@app.get("/api/protected")
async def protected_endpoint(current_user: dict = Depends(get_current_user)):
    """Protected endpoint requiring authentication."""
    logger.info(f"Protected endpoint accessed by user {current_user['user_id']}")
    return success_response(
        data={"user": current_user},
        message="You are authenticated"
    )


# RBAC protected endpoint (requires specific permission)
@app.get("/api/projects")
async def get_projects(
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(get_current_user),
    _: None = Depends(require_permission("project.read"))
):
    """Get projects with pagination and RBAC."""
    logger.info(f"User {current_user['user_id']} fetching projects")
    
    # Mock data - replace with actual database query
    projects = [
        {"id": 1, "name": "Project Alpha", "status": "active"},
        {"id": 2, "name": "Project Beta", "status": "completed"},
        {"id": 3, "name": "Project Gamma", "status": "active"},
    ]
    
    total = len(projects)
    
    # Apply pagination
    result = paginate(projects, total, pagination.page, pagination.page_size)
    
    return success_response(data=result, message="Projects retrieved")


# Role-based endpoint (only ADMIN and MANAGER)
@app.delete("/api/projects/{project_id}")
@auth_rate_limit()
async def delete_project(
    request: Request,
    project_id: int,
    current_user: dict = Depends(get_current_user),
    _: None = Depends(require_role(Role.ADMIN, Role.MANAGER))
):
    """Delete project (ADMIN and MANAGER only)."""
    logger.info(f"User {current_user['user_id']} deleting project {project_id}")
    
    # Delete logic here
    
    return success_response(
        data={"project_id": project_id},
        message="Project deleted successfully"
    )


# Example with custom permission check
@app.post("/api/beneficiaries")
async def create_beneficiary(
    current_user: dict = Depends(get_current_user),
    _: None = Depends(require_permission("beneficiary.create"))
):
    """Create beneficiary (requires beneficiary.create permission)."""
    logger.info(f"User {current_user['user_id']} creating beneficiary")
    
    # Create logic here
    
    return success_response(
        data={"id": 1, "name": "New Beneficiary"},
        message="Beneficiary created"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)