from fastapi import HTTPException, Request

from app.core.security import decode_access_token

BEARER_PREFIX = "Bearer "


# Best-effort only: attaches the user id to request.state for logging/tracing.
# Does NOT enforce auth - route-level access control still goes through
# Depends(get_current_user) in app/api/deps.py, so a missing/bad token here is not an error.
async def attach_user_id(request: Request, call_next):
    request.state.user_id = None
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith(BEARER_PREFIX):
        token = auth_header.removeprefix(BEARER_PREFIX)
        try:
            payload = decode_access_token(token)
            request.state.user_id = payload.get("sub")
        except HTTPException:
            pass
    return await call_next(request)
