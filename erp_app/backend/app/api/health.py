"""
Health check and monitoring endpoints
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime
import sys
import os
import psutil

from ..core.database import get_db

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@router.get("/health/detailed", status_code=status.HTTP_200_OK)
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with system information"""
    try:
        # Check database connection
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Get system information
    system_info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "cpu_count": os.cpu_count(),
        "memory_usage": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "percent": psutil.virtual_memory().percent
        },
        "disk_usage": {
            "total": psutil.disk_usage('/').total,
            "free": psutil.disk_usage('/').free,
            "percent": psutil.disk_usage('/').percent
        }
    }
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "database": db_status,
        "system": system_info
    }

@router.get("/metrics", status_code=status.HTTP_200_OK)
async def get_metrics(db: Session = Depends(get_db)):
    """Get application metrics"""
    try:
        # Count records in main tables (simplified example)
        metrics = {
            "users_count": db.execute("SELECT COUNT(*) FROM users").scalar(),
            "leads_count": db.execute("SELECT COUNT(*) FROM leads").scalar(),
            "contacts_count": db.execute("SELECT COUNT(*) FROM contacts").scalar(),
            "deals_count": db.execute("SELECT COUNT(*) FROM deals").scalar(),
            "products_count": db.execute("SELECT COUNT(*) FROM products").scalar(),
        }
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": metrics
        }
    except Exception as e:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "error": f"Unable to retrieve metrics: {str(e)}"
        }
