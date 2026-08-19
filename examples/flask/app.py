"""
Flask Complete Example Application
Demonstrates all boilerplate features integrated together.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

# Authentication
from auth.routes import auth_bp
from middleware.auth_middleware import require_auth, optional_auth

# RBAC
from rbac.authorization import require_permission, require_role
from rbac.roles import Role

# API Utilities
from api.response_handler.response_formatter import success_response
from api.pagination.paginator import paginate
from api.error_handling.flask_error_handler import register_error_handlers
from api.logging.logger_config import setup_logger

# Security
from security.cors.cors_config import get_flask_cors_config
from security.rate_limit.flask_rate_limiter import get_rate_limiter, rate_limit_error_handler


# Setup logger
logger = setup_logger(name="flask_app", level="INFO")

# Create app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Setup CORS
CORS(app, **get_flask_cors_config())

# Setup rate limiter
limiter = get_rate_limiter()
limiter.init_app(app)

# Register error handlers
register_error_handlers(app)

@app.errorhandler(429)
def handle_rate_limit(e):
    return rate_limit_error_handler(e)

# Register blueprints
app.register_blueprint(auth_bp)


# Startup event
@app.before_request
def before_request():
    """Log all requests."""
    logger.info(f"{request.method} {request.path}")


# Health check
@app.route("/health")
@limiter.exempt
def health():
    """Health check endpoint for load balancers."""
    return jsonify({"status": "healthy", "version": "1.0.0"})


# Public endpoint with rate limit
@app.route("/api/public")
@limiter.limit("100 per minute")
def public_endpoint():
    """Public endpoint with rate limiting."""
    logger.info("Public endpoint accessed")
    return jsonify(success_response(
        data={"message": "This is a public endpoint"},
        message="Success"
    ))


# Protected endpoint (requires authentication)
@app.route("/api/protected")
@require_auth
def protected_endpoint(current_user):
    """Protected endpoint requiring authentication."""
    logger.info(f"Protected endpoint accessed by user {current_user['user_id']}")
    return jsonify(success_response(
        data={"user": current_user},
        message="You are authenticated"
    ))


# RBAC protected endpoint (requires specific permission)
@app.route("/api/projects")
@require_auth
@require_permission("project.read")
def get_projects(current_user):
    """Get projects with pagination and RBAC."""
    logger.info(f"User {current_user['user_id']} fetching projects")
    
    # Get pagination params
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 20, type=int)
    
    # Mock data - replace with actual database query
    projects = [
        {"id": 1, "name": "Project Alpha", "status": "active"},
        {"id": 2, "name": "Project Beta", "status": "completed"},
        {"id": 3, "name": "Project Gamma", "status": "active"},
    ]
    
    total = len(projects)
    
    # Apply pagination
    result = paginate(projects, total, page, page_size)
    
    return jsonify(success_response(data=result, message="Projects retrieved"))


# Role-based endpoint (only ADMIN and MANAGER)
@app.route("/api/projects/<int:project_id>", methods=["DELETE"])
@limiter.limit("5 per minute")
@require_auth
@require_role(Role.ADMIN, Role.MANAGER)
def delete_project(current_user, project_id):
    """Delete project (ADMIN and MANAGER only)."""
    logger.info(f"User {current_user['user_id']} deleting project {project_id}")
    
    # Delete logic here
    
    return jsonify(success_response(
        data={"project_id": project_id},
        message="Project deleted successfully"
    ))


# Example with custom permission check
@app.route("/api/beneficiaries", methods=["POST"])
@require_auth
@require_permission("beneficiary.create")
def create_beneficiary(current_user):
    """Create beneficiary (requires beneficiary.create permission)."""
    logger.info(f"User {current_user['user_id']} creating beneficiary")
    
    # Create logic here
    
    return jsonify(success_response(
        data={"id": 1, "name": "New Beneficiary"},
        message="Beneficiary created"
    )), 201


# Optional auth endpoint
@app.route("/api/optional")
@optional_auth
def optional_auth_endpoint(current_user=None):
    """Endpoint with optional authentication."""
    if current_user:
        message = f"Hello {current_user['user_id']}"
    else:
        message = "Hello guest"
    
    return jsonify(success_response(data={"message": message}))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
