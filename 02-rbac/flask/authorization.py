from functools import wraps
from flask import jsonify, g
from typing import List, Callable
from .roles import Role
from .permissions import Permission


class RolePermissionMap:
    """Map roles to their permissions."""
    
    ROLE_PERMISSIONS = {
        Role.ADMIN: ["*"],  # All permissions
        
        Role.MANAGER: [
            "project.*",
            "beneficiary.*",
            Permission.DONATION_READ,
            Permission.DONATION_CREATE,
            Permission.TASK_READ,
            Permission.TASK_CREATE,
            Permission.TASK_UPDATE,
            Permission.REPORT_READ,
            Permission.REPORT_CREATE,
            Permission.USER_READ,
        ],
        
        Role.FIELD_WORKER: [
            Permission.BENEFICIARY_READ,
            Permission.BENEFICIARY_UPDATE,
            Permission.TASK_READ,
            Permission.TASK_UPDATE,
            Permission.PROJECT_READ,
            Permission.REPORT_READ,
        ],
        
        Role.VOLUNTEER: [
            Permission.PROJECT_READ,
            Permission.TASK_READ,
            Permission.TASK_UPDATE,
        ],
    }
    
    @classmethod
    def get_permissions_for_role(cls, role: str) -> List[str]:
        """Get all permissions for a given role."""
        return cls.ROLE_PERMISSIONS.get(role, [])
    
    @classmethod
    def has_permission(cls, role: str, required_permission: str) -> bool:
        """Check if a role has a specific permission."""
        role_permissions = cls.get_permissions_for_role(role)
        
        for permission_pattern in role_permissions:
            if Permission.matches_pattern(required_permission, permission_pattern):
                return True
        
        return False


def require_permission(permission: str) -> Callable:
    """
    Decorator to check if user has required permission.
    Must be used after @require_auth decorator.
    
    Usage:
        @app.route("/projects/<int:project_id>", methods=["DELETE"])
        @require_auth
        @require_permission("project.delete")
        def delete_project(current_user, project_id):
            # Delete project logic
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            user_role = current_user.get("role")
            
            if not user_role:
                return jsonify({"error": "User role not found"}), 403
            
            if not RolePermissionMap.has_permission(user_role, permission):
                return jsonify({
                    "error": "Permission denied",
                    "required": permission
                }), 403
            
            return f(current_user, *args, **kwargs)
        
        return decorated_function
    return decorator


def require_any_permission(*permissions: str) -> Callable:
    """
    Decorator to check if user has ANY of the required permissions.
    
    Usage:
        @app.route("/dashboard")
        @require_auth
        @require_any_permission("project.read", "task.read")
        def dashboard(current_user):
            # Dashboard logic
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            user_role = current_user.get("role")
            
            if not user_role:
                return jsonify({"error": "User role not found"}), 403
            
            for permission in permissions:
                if RolePermissionMap.has_permission(user_role, permission):
                    return f(current_user, *args, **kwargs)
            
            return jsonify({
                "error": "Permission denied",
                "required_one_of": list(permissions)
            }), 403
        
        return decorated_function
    return decorator


def require_role(*roles: Role) -> Callable:
    """
    Decorator to check if user has one of the required roles.
    
    Usage:
        @app.route("/admin/dashboard")
        @require_auth
        @require_role(Role.ADMIN, Role.MANAGER)
        def admin_dashboard(current_user):
            # Admin dashboard logic
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            user_role = current_user.get("role")
            
            if not user_role:
                return jsonify({"error": "User role not found"}), 403
            
            allowed_roles = [role.value for role in roles]
            
            if user_role not in allowed_roles:
                return jsonify({
                    "error": "Access denied",
                    "required_role": allowed_roles
                }), 403
            
            return f(current_user, *args, **kwargs)
        
        return decorated_function
    return decorator
