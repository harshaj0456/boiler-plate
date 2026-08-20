"""Response formatter for consistent API responses."""

from typing import Any, Dict, Optional

def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200,
) -> Dict[str, Any]:
    """
    Format a success response.
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
        
    Returns:
        Formatted response dict
    """
    return {
        "status": "success",
        "message": message,
        "data": data,
        "status_code": status_code
    }

def error_response(
    message: str = "Error",
    error_code: str = "ERROR",
    status_code: int = 400,
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Format an error response.
    
    Args:
        message: Error message
        error_code: Error code identifier
        status_code: HTTP status code
        details: Additional error details
        
    Returns:
        Formatted error response dict
    """
    return {
        "status": "error",
        "message": message,
        "error_code": error_code,
        "status_code": status_code,
        "details": details or {}
    }
