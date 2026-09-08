from fastapi import APIRouter

from app.api.v1.endpoints import (
    authors,
    ingredients,
    product_groups,
    preparation_methods,
    products,
    recipes,
    reports,
    suppliers,
    invoices,
)

router = APIRouter()

router.include_router(products.router, prefix="/products", tags=["products"])
router.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
router.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
router.include_router(authors.router, prefix="/authors", tags=["authors"])
router.include_router(ingredients.router, prefix="/ingredients", tags=["ingredients"])
router.include_router(product_groups.router, prefix="/product-groups", tags=["product-groups"])
router.include_router(preparation_methods.router, prefix="/preparation-methods", tags=["preparation-methods"])
router.include_router(invoices.router, prefix="/invoices", tags=["invoices"])
router.include_router(reports.router, prefix="/reports", tags=["reports"])