from app.repositories.interfaces.authors import IRepository as IAuthorRepository
from app.repositories.interfaces.base import IRepository
from app.repositories.interfaces.dictionaries import IRepository as IDictionaryRepository
from app.repositories.interfaces.ingredients import IRepository as IIngredientRepository
from app.repositories.interfaces.invoices import IRepository as IInvoiceRepository
from app.repositories.interfaces.products import IRepository as IProductRepository
from app.repositories.interfaces.recipes import IRepository as IRecipeRepository
from app.repositories.interfaces.suppliers import IRepository as ISupplierRepository
from app.repositories.sqlalchemy.authors import AuthorRepository
from app.repositories.sqlalchemy.dictionaries import ProductGroupRepository, PreparationMethodRepository
from app.repositories.sqlalchemy.ingredients import IngredientRepository
from app.repositories.sqlalchemy.invoices import InvoiceItemRepository, InvoiceRepository
from app.repositories.sqlalchemy.products import ProductRepository
from app.repositories.sqlalchemy.recipes import RecipeRepository
from app.repositories.sqlalchemy.suppliers import SupplierRepository

__all__ = [
    "IAuthorRepository",
    "IDictionaryRepository",
    "IIngredientRepository",
    "IInvoiceRepository",
    "IProductRepository",
    "IRecipeRepository",
    "ISupplierRepository",
    "IRepository",
    "AuthorRepository",
    "IngredientRepository",
    "InvoiceItemRepository",
    "InvoiceRepository",
    "PreparationMethodRepository",
    "ProductGroupRepository",
    "ProductRepository",
    "RecipeRepository",
    "SupplierRepository",
]