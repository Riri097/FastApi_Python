import logging
import time

from fastapi import Request

logger = logging.getLogger("app")


# Runs closest to the route so duration reflects actual route execution time;
# correlation_id/user_id are already on request.state by the time this runs
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    correlation_id = getattr(request.state, "correlation_id", "-")
    user_id = getattr(request.state, "user_id", None)
    logger.info(
        "[%s] %s %s %s %.1fms user=%s",
        correlation_id, request.method, request.url.path, response.status_code, duration_ms, user_id,
    )
    return response
