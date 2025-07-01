"""
Dashboard API Routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Dict, Any

from ..core.database import get_db
from ..core.models import User
from ..modules.crm.models import Lead, Contact, Deal
from ..modules.inventory.models import Product
from ..modules.accounting.models import Invoice, Customer
from ..modules.hr.models import Employee
from ..modules.sales.models import SalesOrder
from .auth import get_current_user

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get dashboard statistics"""
    
    # Date ranges
    today = datetime.now().date()
    this_month_start = today.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
    
    # CRM Stats
    total_leads = db.query(Lead).count()
    new_leads_this_month = db.query(Lead).filter(
        func.date(Lead.created_at) >= this_month_start
    ).count()
    
    total_contacts = db.query(Contact).count()
    total_deals = db.query(Deal).count()
    
    # Calculate total deal value
    total_deal_value = db.query(func.sum(Deal.amount)).scalar() or 0
    
    # Inventory Stats
    total_products = db.query(Product).filter(Product.is_active == True).count()
    low_stock_products = db.query(Product).filter(
        and_(Product.track_inventory == True, Product.current_stock <= Product.reorder_level)
    ).count()
    
    # Accounting Stats
    total_customers = db.query(Customer).filter(Customer.is_active == True).count()
    total_invoices = db.query(Invoice).count()
    
    # Calculate revenue
    total_revenue = db.query(func.sum(Invoice.total_amount)).filter(
        Invoice.status == "paid"
    ).scalar() or 0
    
    this_month_revenue = db.query(func.sum(Invoice.total_amount)).filter(
        and_(
            Invoice.status == "paid",
            func.date(Invoice.issue_date) >= this_month_start
        )
    ).scalar() or 0
    
    # Outstanding amount
    outstanding_amount = db.query(func.sum(Invoice.balance_due)).filter(
        Invoice.status.in_(["sent", "overdue"])
    ).scalar() or 0
    
    # HR Stats
    total_employees = db.query(Employee).filter(Employee.status == "active").count()
    
    # Sales Stats
    total_orders = db.query(SalesOrder).count()
    this_month_orders = db.query(SalesOrder).filter(
        func.date(SalesOrder.order_date) >= this_month_start
    ).count()
    
    return {
        "crm": {
            "total_leads": total_leads,
            "new_leads_this_month": new_leads_this_month,
            "total_contacts": total_contacts,
            "total_deals": total_deals,
            "total_deal_value": float(total_deal_value)
        },
        "inventory": {
            "total_products": total_products,
            "low_stock_products": low_stock_products
        },
        "accounting": {
            "total_customers": total_customers,
            "total_invoices": total_invoices,
            "total_revenue": float(total_revenue),
            "this_month_revenue": float(this_month_revenue),
            "outstanding_amount": float(outstanding_amount)
        },
        "hr": {
            "total_employees": total_employees
        },
        "sales": {
            "total_orders": total_orders,
            "this_month_orders": this_month_orders
        }
    }

@router.get("/recent-activities")
async def get_recent_activities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get recent activities across all modules"""
    
    activities = []
    
    # Recent leads
    recent_leads = db.query(Lead).order_by(Lead.created_at.desc()).limit(5).all()
    for lead in recent_leads:
        activities.append({
            "type": "lead_created",
            "title": f"New lead: {lead.first_name} {lead.last_name}",
            "description": f"From {lead.company or 'Unknown Company'}",
            "timestamp": lead.created_at,
            "module": "CRM"
        })
    
    # Recent orders
    recent_orders = db.query(SalesOrder).order_by(SalesOrder.created_at.desc()).limit(5).all()
    for order in recent_orders:
        activities.append({
            "type": "order_created",
            "title": f"New order: {order.order_number}",
            "description": f"Amount: ${order.total_amount}",
            "timestamp": order.created_at,
            "module": "Sales"
        })
    
    # Recent invoices
    recent_invoices = db.query(Invoice).order_by(Invoice.created_at.desc()).limit(5).all()
    for invoice in recent_invoices:
        activities.append({
            "type": "invoice_created",
            "title": f"New invoice: {invoice.invoice_number}",
            "description": f"Amount: ${invoice.total_amount}",
            "timestamp": invoice.created_at,
            "module": "Accounting"
        })
    
    # Sort by timestamp and limit
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    return activities[:limit]

@router.get("/charts/revenue")
async def get_revenue_chart_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    months: int = 12
):
    """Get revenue chart data for the last N months"""
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=months * 30)
    
    # Query monthly revenue
    monthly_revenue = db.query(
        func.strftime('%Y-%m', Invoice.issue_date).label('month'),
        func.sum(Invoice.total_amount).label('revenue')
    ).filter(
        and_(
            Invoice.status == "paid",
            Invoice.issue_date >= start_date
        )
    ).group_by(
        func.strftime('%Y-%m', Invoice.issue_date)
    ).order_by('month').all()
    
    return {
        "labels": [row.month for row in monthly_revenue],
        "data": [float(row.revenue) for row in monthly_revenue]
    }

@router.get("/charts/sales-pipeline")
async def get_sales_pipeline_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get sales pipeline data"""
    
    pipeline_data = db.query(
        Deal.stage,
        func.count(Deal.id).label('count'),
        func.sum(Deal.amount).label('total_value')
    ).group_by(Deal.stage).all()
    
    return {
        "stages": [row.stage for row in pipeline_data],
        "counts": [row.count for row in pipeline_data],
        "values": [float(row.total_value or 0) for row in pipeline_data]
    }
