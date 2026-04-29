from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes.health import router as health_router
from app.api.routes.simplify import router as simplify_router
from app.middleware.trace_id import TraceIDMiddleware
from app.observability.logging_config import configure_observability_logging

configure_observability_logging()

app = FastAPI()

# Register middleware
app.add_middleware(TraceIDMiddleware)


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(
    request: Request,
    exc: RequestValidationError,
):
    """
    Return a stable validation error shape.

    Keeps invalid input responses concise and traceable.
    """
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "invalid_input",
                "message": "Request validation failed.",
            },
            "trace_id": request.state.trace_id,
        },
    )


# Register baseline routes
app.include_router(health_router)
app.include_router(simplify_router)
