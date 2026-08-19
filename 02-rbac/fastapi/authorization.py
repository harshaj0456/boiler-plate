from typing import List, Dict
from fastapi import HTTPException, status, Depends
from .roles import Role
from .permissions import Permission


class RolePermissionMap:
    """Map roles to their permissions."""
    
    ROLE_PERMISSIONS: Dict[str, List[str]] = {
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


def require_permission(required_permission: str):
    """
    Dependency to check if user has required permission.
    
    Usage:
        @app.delete("/projects/{project_id}")
        async def delete_project(
            project_id: int,
            current_user: dict = Depends(get_current_user),
            _: None = Depends(require_permission("project.delete"))
        ):
            # Delete project logic
    """
    async def check_permission(current_user: dict) -> None:
        user_role = current_user.get("role")
        
        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User role not found"
            )
        
        if not RolePermissionMap.has_permission(user_role, required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied. Required: {required_permission}"
            )
    
    return check_permission


def require_any_permission(*permissions: str):
    """
    Dependency to check if user has ANY of the required permissions.
    
    Usage:
        @app.get("/dashboard")
        async def dashboard(
            current_user: dict = Depends(get_current_user),
            _: None = Depends(require_any_permission("project.read", "task.read"))
        ):
            # Dashboard logic
    """
    async def check_permissions(current_user: dict) -> None:
        user_role = current_user.get("role")
        
        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User role not found"
            )
        
        for permission in permissions:
            if RolePermissionMap.has_permission(user_role, permission):
                return
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied. Required one of: {', '.join(permissions)}"
        )
    
    return check_permissions


def require_role(*roles: Role):
    """
    Dependency to check if user has one of the required roles.
    
    Usage:
        @app.get("/admin/dashboard")
        async def admin_dashboard(
            current_user: dict = Depends(get_current_user),
            _: None = Depends(require_role(Role.ADMIN, Role.MANAGER))
        ):
            # Admin dashboard logic
    """
    async def check_role(current_user: dict) -> None:
        user_role = current_user.get("role")
        
        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User role not found"
            )
        
        allowed_roles = [role.value for role in roles]
        
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {', '.join(allowed_roles)}"
            )
    
    return check_role
