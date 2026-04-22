from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class TraceIDMiddleware(BaseHTTPMiddleware):
    """
    Attach a per-request trace identifier.

    This creates a minimal observability baseline without
    introducing logging or external tracing dependencies yet.
    """

    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid4())

        # Store trace id on request state for route handlers
        request.state.trace_id = trace_id

        response = await call_next(request)

        # Return trace id to callers for correlation
        response.headers["X-Trace-ID"] = trace_id
        return response
