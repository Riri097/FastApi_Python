import uuid

from fastapi import Request

REQUEST_ID_HEADER = "X-Request-ID"


# Tags each request with an ID (reusing the client's if they sent one) so every
# log line for the same request can be tied together; echoes it back in the response
async def add_correlation_id(request: Request, call_next):
    correlation_id = request.headers.get(REQUEST_ID_HEADER, str(uuid.uuid4()))
    request.state.correlation_id = correlation_id
    response = await call_next(request)
    response.headers[REQUEST_ID_HEADER] = correlation_id
    return response
