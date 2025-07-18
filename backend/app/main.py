from fastapi import FastAPI
from backend.app.api.routes import auth_routes
from app.database import Base, engine
from backend.app.api import people_routes, product_routes
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NailyManagement")




app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)