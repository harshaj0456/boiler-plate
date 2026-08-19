from typing import List


class Permission:
    """Permission constants using resource.action pattern."""
    
    # Project permissions
    PROJECT_READ = "project.read"
    PROJECT_CREATE = "project.create"
    PROJECT_UPDATE = "project.update"
    PROJECT_DELETE = "project.delete"
    
    # Beneficiary permissions
    BENEFICIARY_READ = "beneficiary.read"
    BENEFICIARY_CREATE = "beneficiary.create"
    BENEFICIARY_UPDATE = "beneficiary.update"
    BENEFICIARY_DELETE = "beneficiary.delete"
    
    # Donation permissions
    DONATION_READ = "donation.read"
    DONATION_CREATE = "donation.create"
    DONATION_UPDATE = "donation.update"
    DONATION_DELETE = "donation.delete"
    
    # Task permissions
    TASK_READ = "task.read"
    TASK_CREATE = "task.create"
    TASK_UPDATE = "task.update"
    TASK_DELETE = "task.delete"
    
    # User management permissions
    USER_READ = "user.read"
    USER_CREATE = "user.create"
    USER_UPDATE = "user.update"
    USER_DELETE = "user.delete"
    
    # Report permissions
    REPORT_READ = "report.read"
    REPORT_CREATE = "report.create"
    
    @classmethod
    def all_permissions(cls) -> List[str]:
        """Get list of all permissions."""
        return [
            value for name, value in vars(cls).items()
            if not name.startswith("_") and isinstance(value, str)
        ]
    
    @classmethod
    def get_resource_permissions(cls, resource: str) -> List[str]:
        """Get all permissions for a specific resource."""
        return [
            value for value in cls.all_permissions()
            if value.startswith(f"{resource}.")
        ]
    
    @classmethod
    def matches_pattern(cls, permission: str, pattern: str) -> bool:
        """
        Check if permission matches a pattern.
        Supports wildcards: project.* matches all project permissions.
        """
        if pattern == "*":
            return True
        
        if pattern.endswith(".*"):
            resource = pattern[:-2]
            return permission.startswith(f"{resource}.")
        
        return permission == pattern
