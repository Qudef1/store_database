from app.services.interfaces.authors import ICrudService as IAuthorService
from app.services.interfaces.base import ICrudService
from app.services.interfaces.dictionaries import ICrudService as IDictionaryService
from app.services.interfaces.ingredients import ICrudService as IIngredientService
from app.services.interfaces.invoices import ICrudService as IInvoiceService
from app.services.interfaces.products import ICrudService as IProductService
from app.services.interfaces.recipes import ICrudService as IRecipeService
from app.services.interfaces.reports import (
    IMinCalorieProductsService,
    IProductRecipesService,
    ISupplierPriceListService,
)
from app.services.interfaces.suppliers import ICrudService as ISupplierService
from app.services.implementations.products import ProductService
from app.services.implementations.recipes import RecipeService
from app.services.implementations.suppliers import SupplierService
from app.services.implementations.reports import (
    MinCalorieProductsService,
    ProductRecipesService,
    SupplierPriceListService,
)

__all__ = [
    "IAuthorService",
    "IDictionaryService",
    "IIngredientService",
    "IInvoiceService",
    "IProductService",
    "IRecipeService",
    "ISupplierService",
    "IMinCalorieProductsService",
    "IProductRecipesService",
    "ISupplierPriceListService",
    "ProductService",
    "RecipeService",
    "SupplierService",
    "MinCalorieProductsService",
    "ProductRecipesService",
    "SupplierPriceListService",
]