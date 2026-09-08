from app.services.interfaces.base import ICrudService
from app.models import Ingredient
from app.schemas.ingredients import IngredientCreate, IngredientRead, IngredientUpdate

__all__ = [
    "ICrudService",
    "Ingredient",
    "IngredientCreate",
    "IngredientRead",
    "IngredientUpdate",
]