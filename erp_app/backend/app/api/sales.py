"""
Sales API Routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..core.models import User
from ..modules.sales.models import Quote, SalesOrder, Shipment
from .auth import get_current_user

router = APIRouter()

@router.get("/quotes")
async def get_quotes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None
):
    """Get all quotes"""
    query = db.query(Quote)
    
    if status:
        query = query.filter(Quote.status == status)
    
    quotes = query.order_by(Quote.created_at.desc()).offset(skip).limit(limit).all()
    total = query.count()
    
    return {
        "quotes": [
            {
                "id": quote.id,
                "quote_number": quote.quote_number,
                "customer_id": quote.customer_id,
                "quote_date": quote.quote_date,
                "valid_until": quote.valid_until,
                "total_amount": float(quote.total_amount),
                "status": quote.status
            }
            for quote in quotes
        ],
        "total": total
    }

@router.post("/quotes")
async def create_quote(
    quote_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new quote"""
    new_quote = Quote(
        quote_number=quote_data["quote_number"],
        customer_id=quote_data["customer_id"],
        quote_date=quote_data["quote_date"],
        valid_until=quote_data["valid_until"],
        subtotal=quote_data.get("subtotal", 0),
        tax_amount=quote_data.get("tax_amount", 0),
        total_amount=quote_data.get("total_amount", 0),
        notes=quote_data.get("notes"),
        sales_rep_id=quote_data.get("sales_rep_id"),
        created_by=current_user.id
    )
    
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    
    return {"message": "Quote created successfully", "quote_id": new_quote.id}

@router.get("/orders")
async def get_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None
):
    """Get all sales orders"""
    query = db.query(SalesOrder)
    
    if status:
        query = query.filter(SalesOrder.status == status)
    
    orders = query.order_by(SalesOrder.created_at.desc()).offset(skip).limit(limit).all()
    total = query.count()
    
    return {
        "orders": [
            {
                "id": order.id,
                "order_number": order.order_number,
                "customer_id": order.customer_id,
                "order_date": order.order_date,
                "required_date": order.required_date,
                "total_amount": float(order.total_amount),
                "status": order.status
            }
            for order in orders
        ],
        "total": total
    }

@router.post("/orders")
async def create_order(
    order_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new sales order"""
    new_order = SalesOrder(
        order_number=order_data["order_number"],
        customer_id=order_data["customer_id"],
        order_date=order_data["order_date"],
        required_date=order_data.get("required_date"),
        subtotal=order_data.get("subtotal", 0),
        tax_amount=order_data.get("tax_amount", 0),
        total_amount=order_data.get("total_amount", 0),
        shipping_address=order_data.get("shipping_address"),
        notes=order_data.get("notes"),
        sales_rep_id=order_data.get("sales_rep_id"),
        created_by=current_user.id
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    return {"message": "Sales order created successfully", "order_id": new_order.id}

@router.get("/shipments")
async def get_shipments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all shipments"""
    shipments = db.query(Shipment).order_by(Shipment.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "shipments": [
            {
                "id": shipment.id,
                "shipment_number": shipment.shipment_number,
                "order_id": shipment.order_id,
                "ship_date": shipment.ship_date,
                "carrier": shipment.carrier,
                "tracking_number": shipment.tracking_number,
                "shipping_cost": float(shipment.shipping_cost) if shipment.shipping_cost else 0
            }
            for shipment in shipments
        ]
    }
