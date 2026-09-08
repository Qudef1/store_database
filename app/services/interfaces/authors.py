from app.services.interfaces.base import ICrudService
from app.models import Author
from app.schemas.authors import AuthorCreate, AuthorRead, AuthorUpdate

__all__ = [
    "ICrudService",
    "Author",
    "AuthorCreate",
    "AuthorRead",
    "AuthorUpdate",
]