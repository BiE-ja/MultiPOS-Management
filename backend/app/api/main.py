from fastapi import APIRouter

from backend.app.api.routes.deps import auth_routes
from backend.app.api.routes.operation import product_routes

api_routeur = APIRouter()

api_routeur.include_router(auth_routes.router, prefix="/auth", tags=["auth"] )
api_routeur.include_router(product_routes.router, prefix="/product", tags=["product"])
