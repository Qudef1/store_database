from fastapi import APIRouter

from app.api.v1.endpoints import products, recipes, suppliers, reports

router = APIRouter()

router.include_router(products.router, prefix="/products", tags=["products"])
router.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
router.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
router.include_router(reports.router, prefix="/reports", tags=["reports"])