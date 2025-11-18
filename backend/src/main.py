from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sentry_sdk
from contextlib import asynccontextmanager

from src.config import settings
from src.api import content, analytics, campaigns, social_accounts


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    if settings.sentry_dsn:
        sentry_sdk.init(dsn=settings.sentry_dsn, environment=settings.app_env)

    print(f"🚀 {settings.app_name} starting up...")
    yield
    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title=settings.app_name,
    description="AI-powered marketing automation platform",
    version=settings.api_version,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name} API",
        "version": settings.api_version,
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "environment": settings.app_env}
    )


# Include routers
app.include_router(content.router, prefix=f"/api/{settings.api_version}/content", tags=["Content"])
app.include_router(analytics.router, prefix=f"/api/{settings.api_version}/analytics", tags=["Analytics"])
app.include_router(campaigns.router, prefix=f"/api/{settings.api_version}/campaigns", tags=["Campaigns"])
app.include_router(social_accounts.router, prefix=f"/api/{settings.api_version}/social-accounts", tags=["Social Accounts"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
