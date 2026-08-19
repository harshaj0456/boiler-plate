from typing import List, TypeVar, Generic
from pydantic import BaseModel
from math import ceil

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination query parameters."""
    page: int = 1
    page_size: int = 20
    
    def get_offset(self) -> int:
        """Calculate offset for database query."""
        return (self.page - 1) * self.page_size
    
    def get_limit(self) -> int:
        """Get limit for database query."""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
    
    class Config:
        arbitrary_types_allowed = True


def paginate(
    items: List[T],
    total: int,
    page: int,
    page_size: int
) -> PaginatedResponse[T]:
    """
    Create a paginated response.
    
    Args:
        items: List of items for current page
        total: Total number of items
        page: Current page number
        page_size: Items per page
    
    Returns:
        PaginatedResponse with pagination metadata
    """
    total_pages = ceil(total / page_size) if page_size > 0 else 0
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


# Example usage with SQLAlchemy
def paginate_query(query, page: int = 1, page_size: int = 20):
    """
    Paginate a SQLAlchemy query.
    
    Usage:
        from sqlalchemy.orm import Session
        
        def get_users(db: Session, page: int, page_size: int):
            query = db.query(User)
            return paginate_query(query, page, page_size)
    """
    total = query.count()
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    
    return paginate(items, total, page, page_size)
