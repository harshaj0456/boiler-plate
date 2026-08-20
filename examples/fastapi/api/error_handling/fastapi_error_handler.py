"""FastAPI error handlers."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from api.response_handler.response_formatter import error_response
import logging

logger = logging.getLogger(__name__)

def register_exception_handlers(app: FastAPI):
    """
    Register exception handlers for FastAPI app.
    
    Args:
        app: FastAPI application instance
    """
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        """Handle HTTP exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(
                message=exc.detail,
                status_code=exc.status_code,
                error_code="HTTP_EXCEPTION"
            )
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request, exc):
        """Handle value errors."""
        logger.error(f"ValueError: {str(exc)}")
        return JSONResponse(
            status_code=400,
            content=error_response(
                message="Invalid value provided",
                status_code=400,
                error_code="VALUE_ERROR",
                details={"error": str(exc)}
            )
        )
    
    @app.exception_handler(Exception)
    async def generic_exception_handler(request, exc):
        """Handle generic exceptions."""
        logger.error(f"Unhandled exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content=error_response(
                message="Internal server error",
                status_code=500,
                error_code="INTERNAL_SERVER_ERROR"
            )
        )
