from fastapi import APIRouter

from backend.app.api.routes import auth_routes, people_routes, product_routes

api_routeur = APIRouter()

api_routeur.include_router(auth_routes.router, prefix="/auth", tags=["auth"] )
api_routeur.include_router(product_routes.router, prefix="/product", tags=["product"])
api_routeur.include_router(people_routes.router, prefix="/customer", tags=["customer"])