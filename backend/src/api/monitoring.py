from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict
import psutil
import platform

from src.config import settings
from src.models.database import get_db, engine

router = APIRouter()


@router.get("/health/live")
async def liveness_check() -> Dict:
    """Kubernetes liveness probe"""
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness_check(db: Session = Depends(get_db)) -> Dict:
    """Kubernetes readiness probe - checks all dependencies"""
    health_status = {
        "status": "ready",
        "checks": {}
    }

    # Check database
    try:
        db.execute("SELECT 1")
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["status"] = "not_ready"
        health_status["checks"]["database"] = f"unhealthy: {str(e)}"

    # Check Redis (if configured)
    try:
        from redis import Redis
        redis_client = Redis.from_url(settings.redis_url)
        redis_client.ping()
        health_status["checks"]["redis"] = "healthy"
    except Exception as e:
        health_status["status"] = "not_ready"
        health_status["checks"]["redis"] = f"unhealthy: {str(e)}"

    return health_status


@router.get("/metrics")
async def metrics() -> Dict:
    """Prometheus-style metrics"""

    # System metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return {
        "system": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available_mb": memory.available / (1024 * 1024),
            "disk_percent": disk.percent,
            "disk_free_gb": disk.free / (1024 * 1024 * 1024)
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "python_version": platform.python_version()
        },
        "application": {
            "name": settings.app_name,
            "version": settings.api_version,
            "environment": settings.app_env
        }
    }


@router.get("/info")
async def application_info() -> Dict:
    """Application information"""
    return {
        "name": settings.app_name,
        "version": settings.api_version,
        "environment": settings.app_env,
        "debug": settings.debug,
        "features": {
            "ai_content_generation": True,
            "image_generation": bool(settings.replicate_api_token),
            "email_notifications": bool(settings.sendgrid_api_key),
            "payments": bool(settings.stripe_secret_key),
            "social_media_publishing": True
        }
    }
