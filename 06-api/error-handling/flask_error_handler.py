from flask import jsonify, request
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)


class APIException(Exception):
    """Base API Exception."""
    
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundException(APIException):
    """Resource not found exception."""
    
    def __init__(self, message: str = "Resource not found", details: dict = None):
        super().__init__(message, 404, details)


class UnauthorizedException(APIException):
    """Unauthorized access exception."""
    
    def __init__(self, message: str = "Unauthorized", details: dict = None):
        super().__init__(message, 401, details)


class ForbiddenException(APIException):
    """Forbidden access exception."""
    
    def __init__(self, message: str = "Forbidden", details: dict = None):
        super().__init__(message, 403, details)


class BadRequestException(APIException):
    """Bad request exception."""
    
    def __init__(self, message: str = "Bad request", details: dict = None):
        super().__init__(message, 400, details)


class ConflictException(APIException):
    """Conflict exception."""
    
    def __init__(self, message: str = "Conflict", details: dict = None):
        super().__init__(message, 409, details)


def handle_api_exception(error: APIException):
    """Handle custom API exceptions."""
    logger.error(f"API Exception: {error.message}", extra={
        "status_code": error.status_code,
        "details": error.details,
        "path": request.path,
        "method": request.method
    })
    
    response = jsonify({
        "error": error.message,
        "details": error.details,
        "path": request.path
    })
    response.status_code = error.status_code
    return response


def handle_validation_error(error: ValidationError):
    """Handle Marshmallow validation errors."""
    logger.warning(f"Validation error: {error.messages}", extra={
        "path": request.path,
        "method": request.method
    })
    
    response = jsonify({
        "error": "Validation error",
        "details": error.messages,
        "path": request.path
    })
    response.status_code = 422
    return response


def handle_404_error(error):
    """Handle 404 errors."""
    logger.warning(f"404 Not Found: {request.path}")
    
    response = jsonify({
        "error": "Not Found",
        "message": f"The requested URL {request.path} was not found",
        "path": request.path
    })
    response.status_code = 404
    return response


def handle_500_error(error):
    """Handle 500 errors."""
    logger.exception(f"Internal server error: {str(error)}", extra={
        "path": request.path,
        "method": request.method
    })
    
    response = jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "path": request.path
    })
    response.status_code = 500
    return response


def register_error_handlers(app):
    """Register all error handlers."""
    app.register_error_handler(APIException, handle_api_exception)
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(404, handle_404_error)
    app.register_error_handler(500, handle_500_error)
