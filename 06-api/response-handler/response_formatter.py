from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel


class APIResponse(BaseModel):
    """Standard API response format."""
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    timestamp: str
    
    class Config:
        arbitrary_types_allowed = True


def success_response(
    data: Any = None,
    message: str = "Success"
) -> dict:
    """
    Create a success response.
    
    Usage:
        @app.get("/users/{user_id}")
        async def get_user(user_id: int):
            user = get_user_from_db(user_id)
            return success_response(data=user, message="User retrieved")
    """
    return {
        "success": True,
        "data": data,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }


def error_response(
    message: str = "Error",
    details: Optional[dict] = None
) -> dict:
    """
    Create an error response.
    
    Usage:
        @app.get("/users/{user_id}")
        async def get_user(user_id: int):
            user = get_user_from_db(user_id)
            if not user:
                return error_response(
                    message="User not found",
                    details={"user_id": user_id}
                )
    """
    response = {
        "success": False,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if details:
        response["details"] = details
    
    return response


def created_response(
    data: Any,
    message: str = "Resource created"
) -> dict:
    """
    Create a 201 Created response.
    
    Usage:
        @app.post("/users")
        async def create_user(user_data: UserCreate):
            user = create_user_in_db(user_data)
            return created_response(data=user, message="User created")
    """
    return {
        "success": True,
        "data": data,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }


def no_content_response(message: str = "Operation successful") -> dict:
    """
    Create a 204 No Content response.
    
    Usage:
        @app.delete("/users/{user_id}")
        async def delete_user(user_id: int):
            delete_user_from_db(user_id)
            return no_content_response(message="User deleted")
    """
    return {
        "success": True,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
