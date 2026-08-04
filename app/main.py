import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, users
from app.db.session import Base, engine
from app.middleware.auth import attach_user_id
from app.middleware.correlation_id import add_correlation_id
from app.middleware.exception_handler import handle_unhandled_exception
from app.middleware.logging import log_requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


# Create tables on startup instead of using Alembic, simplest option for this project
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="College Management System", lifespan=lifespan)

# Registered innermost-first: each call wraps the next, so the LAST one added here
# runs FIRST on the way in. Order below gives: CORS -> correlation_id -> auth -> logging -> route.
app.middleware("http")(log_requests)
app.middleware("http")(attach_user_id)
app.middleware("http")(add_correlation_id)
# CORS: wide open for local dev since there's no frontend origin decided yet - narrow this before deploying
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(Exception, handle_unhandled_exception)

app.include_router(auth.router)
app.include_router(users.router)
