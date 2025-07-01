"""
Main API Router
"""
from fastapi import APIRouter

from .auth import router as auth_router
from .crm import router as crm_router
from .inventory import router as inventory_router
from .accounting import router as accounting_router
from .hr import router as hr_router
from .sales import router as sales_router
from .dashboard import router as dashboard_router
from .health import router as health_router

api_router = APIRouter()

# Include all module routers
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(crm_router, prefix="/crm", tags=["CRM"])
api_router.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(accounting_router, prefix="/accounting", tags=["Accounting"])
api_router.include_router(hr_router, prefix="/hr", tags=["Human Resources"])
api_router.include_router(sales_router, prefix="/sales", tags=["Sales"])
