from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
import sentry_sdk
from app.core.config import settings
from app.initial_data import main
from app.api.main import api_router

# Base.metadata.create_all(bind=engine) A EFFACER

from contextlib import asynccontextmanager

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await main()
    yield

if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(
        dsn=str(settings.SENTRY_DSN),
        enable_tracing=True,
    )


app = FastAPI(
    title=settings.PROJECT_NAME, 
    openapi_url=f"{settings.API_V01_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    version="0.1.0",
    lifespan=lifespan
    )

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
# Include your routers here
app.include_router(api_router, prefix=settings.API_V01_STR)

