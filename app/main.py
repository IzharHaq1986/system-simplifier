from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.simplify import router as simplify_router
from app.middleware.trace_id import TraceIDMiddleware

app = FastAPI()

# Register middleware
app.add_middleware(TraceIDMiddleware)

# Register baseline routes
app.include_router(health_router)
app.include_router(simplify_router)
