from app.schemas.base import BaseSchema, ErrorResponse, IdResponse, MessageResponse, Page
from app.schemas.dictionaries import (
    PreparationMethodBase,
    PreparationMethodCreate,
    PreparationMethodRead,
    PreparationMethodUpdate,
    ProductGroupBase,
    ProductGroupCreate,
    ProductGroupRead,
    ProductGroupUpdate,
)
from app.schemas.queries import (
    DishWithRecipesQuery,
    IngredientListQuery,
    InvoiceListQuery,
    MinCalorieDishesQuery,
    PaginationQuery,
    PriceListQuery,
    ProductListQuery,
    RecipeListQuery,
    SupplierListQuery,
)
from app.schemas.reports import (
    DishCalorieRead,
    DishRecipeRead,
    DishWithRecipes,
    MinCalorieDishesResponse,
    PriceListItem,
    PriceListResponse,
)
from app.schemas.authors import (
    AuthorBase,
    AuthorCreate,
    AuthorRead,
    AuthorUpdate,
)
from app.schemas.ingredients import (
    IngredientBase,
    IngredientCreate,
    IngredientRead,
    IngredientShort,
    IngredientUpdate,
)
from app.schemas.suppliers import (
    SupplierBase,
    SupplierCreate,
    SupplierRead,
    SupplierUpdate,
)
from app.schemas.products import (
    ProductBase,
    ProductCreate,
    ProductRead,
    ProductShort,
    ProductUpdate,
    ProductWithRecipes,
)
from app.schemas.recipes import (
    RecipeBase,
    RecipeCreate,
    RecipeIngredientBase,
    RecipeIngredientCreate,
    RecipeIngredientRead,
    RecipeIngredientUpdate,
    RecipeListRead,
    RecipeRead,
    RecipeTitle,
    RecipeUpdate,
)
from app.schemas.invoices import (
    InvoiceBase,
    InvoiceCreate,
    InvoiceItemBase,
    InvoiceItemCreate,
    InvoiceItemRead,
    InvoiceItemUpdate,
    InvoiceRead,
    InvoiceUpdate,
)