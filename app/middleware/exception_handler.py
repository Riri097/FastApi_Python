import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("app")


# Catches anything a route didn't handle so clients get JSON, not a raw traceback
async def handle_unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
