from fastapi import APIRouter

from app.api.routes import (
    login, private, sale_routes, supplier_routes, log_routes)
from app.core.config import settings
from backend.app.api.routes.finance import finance_routes
from backend.app.api.routes.management import area, employee, user
from backend.app.api.routes.operation import customer_routes
from backend.app.api.routes.operation.product import category, product
from backend.app.api.routes.operation.stock import movement

api_router = APIRouter()

api_router.include_router(login.router)
api_router.include_router(category.router)
api_router.include_router(product.router)
api_router.include_router(movement.router)

api_router.include_router(employee.router)
api_router.include_router(area.router)
api_router.include_router(user.router)
api_router.include_router(finance_routes.router)
api_router.include_router(sale_routes.router)
api_router.include_router(supplier_routes.router)
api_router.include_router(customer_routes.router)
api_router.include_router(log_routes.router)

if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
