from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import events, analytics, tenants, auth
from datetime import datetime, timezone
from app.core.logging import setup_logging
import logging

# Configure logging for slow queries
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log all SQLAlchemy queries slower than 1 second
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

loggger = setup_logging()
# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)


# CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Analytics API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
  """Health check endpoint for load balancers."""
  loggger.info("Health check requested.")
  return {
    'status':'healthy',
    'timestamp' : datetime.now(timezone.utc).strftime('%Y-%m-%d')
    }
  
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["authentication"])
app.include_router(tenants.router, prefix=f"{settings.API_V1_PREFIX}/tenants", tags=["tenants"])
app.include_router(events.router, prefix=f"{settings.API_V1_PREFIX}/events", tags=["events"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_PREFIX}/analytics", tags=["analytics"])