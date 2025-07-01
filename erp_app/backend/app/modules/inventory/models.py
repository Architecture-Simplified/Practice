"""
Inventory Management Models
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime

from ...core.database import Base

class ProductType(str, enum.Enum):
    GOODS = "goods"
    SERVICE = "service"
    DIGITAL = "digital"

class StockMovementType(str, enum.Enum):
    IN = "in"
    OUT = "out"
    ADJUSTMENT = "adjustment"

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Self-referential relationship for hierarchical categories
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    type = Column(Enum(ProductType), default=ProductType.GOODS)
    category_id = Column(Integer, ForeignKey("categories.id"))
    brand = Column(String(100))
    
    # Pricing
    cost_price = Column(Numeric(10, 2))
    selling_price = Column(Numeric(10, 2))
    currency = Column(String(3), default="USD")
    
    # Inventory
    track_inventory = Column(Boolean, default=True)
    current_stock = Column(Integer, default=0)
    minimum_stock = Column(Integer, default=0)
    maximum_stock = Column(Integer)
    reorder_level = Column(Integer, default=0)
    
    # Physical attributes
    weight = Column(Numeric(8, 2))  # in kg
    dimensions = Column(String(100))  # LxWxH
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # SEO and images
    image_url = Column(String(500))
    barcode = Column(String(50))
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    category = relationship("Category", back_populates="products")
    stock_movements = relationship("StockMovement", back_populates="product")
    warehouse_stocks = relationship("WarehouseStock", back_populates="product")

class Warehouse(Base):
    __tablename__ = "warehouses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    address = Column(Text)
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    postal_code = Column(String(20))
    phone = Column(String(20))
    email = Column(String(100))
    manager_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    stocks = relationship("WarehouseStock", back_populates="warehouse")
    stock_movements = relationship("StockMovement", back_populates="warehouse")

class WarehouseStock(Base):
    __tablename__ = "warehouse_stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)
    available_quantity = Column(Integer, default=0)
    location = Column(String(50))  # Aisle, Shelf, Bin location
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    warehouse = relationship("Warehouse", back_populates="stocks")
    product = relationship("Product", back_populates="warehouse_stocks")

class StockMovement(Base):
    __tablename__ = "stock_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    movement_type = Column(Enum(StockMovementType))
    quantity = Column(Integer, nullable=False)
    reference_number = Column(String(50))  # PO number, invoice number, etc.
    reason = Column(String(200))
    notes = Column(Text)
    
    # Before and after quantities for audit
    quantity_before = Column(Integer)
    quantity_after = Column(Integer)
    
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="stock_movements")
    warehouse = relationship("Warehouse", back_populates="stock_movements")

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    contact_person = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    website = Column(String(200))
    address = Column(Text)
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    postal_code = Column(String(20))
    tax_number = Column(String(50))
    payment_terms = Column(String(100))
    credit_limit = Column(Numeric(15, 2))
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
