from fastapi import FastAPI
from fastapi import APIRouter

def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Scaffold",
        version="0.0.1",
        description="A scaffold for building FastAPI applications.",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    router = APIRouter(prefix="/api/v1")

    @router.get("/health")
    async def health_check():
        return {"status": "healthy", "version": "0.0.1"}
    
    app.include_router(router)

    return app
app = create_app()