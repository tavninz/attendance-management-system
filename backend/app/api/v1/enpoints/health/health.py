# app/api/v1/endpoints/health.py
import time
import psutil
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api.core.config import settings
from app.api.core.database import get_db, engine

router = APIRouter()

# Track server start time
START_TIME = time.time()

@router.get("/health", tags=["Health Check"])
def health_check(db: Session = Depends(get_db)):
    db_status = "healthy"
    db_latency_ms = 0
    
    try:
        start_db = time.time()
        db.execute(text("SELECT 1"))
        db_latency_ms = round((time.time() - start_db) * 1000, 2)
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    pool = engine.pool
    pool_status = {
        "pool_size": pool.size(),
        "checked_in_connections": pool.checkedin(),
        "checked_out_connections": pool.checkedout(),
        "overflow": pool.overflow(),
    }

    process = psutil.Process()
    memory_usage_mb = round(process.memory_info().rss / 1024 / 1024, 2)
    cpu_percent = process.cpu_percent(interval=None)

    uptime_seconds = round(time.time() - START_TIME, 2)
    is_healthy = db_status == "healthy"

    return {
        "status": "online" if is_healthy else "degraded",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "uptime_seconds": uptime_seconds,
        "system": {
            "cpu_usage_percent": cpu_percent,
            "memory_usage_mb": memory_usage_mb,
        },
        "services": {
            "backend": "running",
            "database": {
                "status": db_status,
                "latency_ms": db_latency_ms,
                "connection_pool": pool_status
            },
            "docker_containers": {
                "postgres": "healthy (via compose healthcheck)",
                "pgadmin": "running"
            },
            "nginx": "pending_proxy_setup",
            "frontend": "pending_setup"
        }
    }