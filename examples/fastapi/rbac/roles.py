"""Role definitions."""

from enum import Enum

class Role(str, Enum):
    """Available roles in the system."""
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"
