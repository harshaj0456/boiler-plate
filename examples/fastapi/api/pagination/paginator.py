"""Pagination utilities."""

from typing import List, Dict, Any
from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(10, ge=1, le=100, description="Items per page")

def paginate(
    items: List[Any],
    total: int,
    page: int = 1,
    page_size: int = 10
) -> Dict[str, Any]:
    """
    Paginate a list of items.
    
    Args:
        items: List of items to paginate
        total: Total count of items
        page: Current page number (1-indexed)
        page_size: Items per page
        
    Returns:
        Paginated response dict
    """
    start = (page - 1) * page_size
    end = start + page_size
    
    paginated_items = items[start:end]
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "items": paginated_items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }
