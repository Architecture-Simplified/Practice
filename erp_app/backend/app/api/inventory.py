"""
Inventory API Routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..core.models import User
from ..modules.inventory.models import Product, Category, Warehouse, StockMovement
from .auth import get_current_user

router = APIRouter()

@router.get("/products")
async def get_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category_id: Optional[int] = None
):
    """Get all products with optional filtering"""
    query = db.query(Product).filter(Product.is_active == True)
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    products = query.offset(skip).limit(limit).all()
    total = query.count()
    
    return {
        "products": [
            {
                "id": product.id,
                "sku": product.sku,
                "name": product.name,
                "type": product.type,
                "cost_price": float(product.cost_price) if product.cost_price else 0,
                "selling_price": float(product.selling_price) if product.selling_price else 0,
                "current_stock": product.current_stock,
                "minimum_stock": product.minimum_stock,
                "is_active": product.is_active
            }
            for product in products
        ],
        "total": total
    }

@router.post("/products")
async def create_product(
    product_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new product"""
    new_product = Product(
        sku=product_data["sku"],
        name=product_data["name"],
        description=product_data.get("description"),
        type=product_data.get("type", "goods"),
        category_id=product_data.get("category_id"),
        brand=product_data.get("brand"),
        cost_price=product_data.get("cost_price"),
        selling_price=product_data.get("selling_price"),
        track_inventory=product_data.get("track_inventory", True),
        minimum_stock=product_data.get("minimum_stock", 0),
        reorder_level=product_data.get("reorder_level", 0)
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return {"message": "Product created successfully", "product_id": new_product.id}

@router.get("/categories")
async def get_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all product categories"""
    categories = db.query(Category).filter(Category.is_active == True).all()
    
    return {
        "categories": [
            {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "parent_id": category.parent_id
            }
            for category in categories
        ]
    }

@router.post("/categories")
async def create_category(
    category_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new category"""
    new_category = Category(
        name=category_data["name"],
        description=category_data.get("description"),
        parent_id=category_data.get("parent_id")
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return {"message": "Category created successfully", "category_id": new_category.id}

@router.get("/warehouses")
async def get_warehouses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all warehouses"""
    warehouses = db.query(Warehouse).filter(Warehouse.is_active == True).all()
    
    return {
        "warehouses": [
            {
                "id": warehouse.id,
                "name": warehouse.name,
                "code": warehouse.code,
                "address": warehouse.address,
                "city": warehouse.city,
                "manager_name": warehouse.manager_name
            }
            for warehouse in warehouses
        ]
    }

@router.get("/stock-movements")
async def get_stock_movements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    product_id: Optional[int] = None
):
    """Get stock movements"""
    query = db.query(StockMovement)
    
    if product_id:
        query = query.filter(StockMovement.product_id == product_id)
    
    movements = query.order_by(StockMovement.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "movements": [
            {
                "id": movement.id,
                "product_id": movement.product_id,
                "warehouse_id": movement.warehouse_id,
                "movement_type": movement.movement_type,
                "quantity": movement.quantity,
                "reference_number": movement.reference_number,
                "reason": movement.reason,
                "created_at": movement.created_at
            }
            for movement in movements
        ]
    }
