from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi import APIRouter
from app.core.config import get_settings
from contextlib import asynccontextmanager


@asynccontextmanager
async  def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    #------startup code------

    # we need to load config variables (Settings).
    settings = get_settings()
    print("Welcome to server")

    #steps will freeze here but the application will be in running state until the shutdown event is triggered.
    yield 

    #------shutdown code------
    print ("Application is shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Scaffold",
        version="0.0.1",
        description="A scaffold for building FastAPI applications.",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )

    router = APIRouter(prefix="/api/v1")

    @router.get("/health")
    async def health_check():
        return {"status": "healthy", "version": "0.0.1"}
    
    app.include_router(router)

    return app
app = create_app()