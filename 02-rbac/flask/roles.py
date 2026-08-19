from enum import Enum


class Role(str, Enum):
    """User roles with hierarchical structure."""
    
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    FIELD_WORKER = "FIELD_WORKER"
    VOLUNTEER = "VOLUNTEER"
    
    @classmethod
    def get_hierarchy(cls) -> dict:
        """
        Get role hierarchy levels.
        Higher numbers = more privileges.
        """
        return {
            cls.VOLUNTEER: 1,
            cls.FIELD_WORKER: 2,
            cls.MANAGER: 3,
            cls.ADMIN: 4
        }
    
    @classmethod
    def has_higher_privilege(cls, role1: str, role2: str) -> bool:
        """Check if role1 has higher privilege than role2."""
        hierarchy = cls.get_hierarchy()
        return hierarchy.get(role1, 0) > hierarchy.get(role2, 0)
    
    @classmethod
    def list_roles(cls) -> list:
        """Get list of all roles."""
        return [role.value for role in cls]
