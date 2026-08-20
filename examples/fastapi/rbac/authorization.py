"""Authorization and permission checking."""

from fastapi import Depends, HTTPException, status
from middleware.auth_middleware import get_current_user
from rbac.roles import Role

def require_permission(*required_permissions: str):
    """
    Dependency to check if user has required permission.
    
    Args:
        required_permissions: Permission strings to check
        
    Returns:
        Dependency function
    """
    async def check_permission(current_user: dict = Depends(get_current_user)):
        user_permissions = set(current_user.get("permissions", []))
        required = set(required_permissions)
        
        if not required.issubset(user_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return None
    
    return check_permission

def require_role(*required_roles: Role):
    """
    Dependency to check if user has required role.
    
    Args:
        required_roles: Role values to check
        
    Returns:
        Dependency function
    """
    async def check_role(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        required_role_values = [role.value if isinstance(role, Role) else role for role in required_roles]
        
        if user_role not in required_role_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {user_role} is not authorized"
            )
        return None
    
    return check_role
