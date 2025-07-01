"""
Sales Module Models
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime

from ...core.database import Base

class QuoteStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Quote(Base):
    __tablename__ = "quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    quote_number = Column(String(50), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    
    # Dates
    quote_date = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    
    # Amounts
    subtotal = Column(Numeric(15, 2), default=0)
    tax_amount = Column(Numeric(15, 2), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    total_amount = Column(Numeric(15, 2), default=0)
    
    currency = Column(String(3), default="USD")
    status = Column(Enum(QuoteStatus), default=QuoteStatus.DRAFT)
    
    # Additional info
    notes = Column(Text)
    terms_and_conditions = Column(Text)
    
    # Sales rep
    sales_rep_id = Column(Integer, ForeignKey("employees.id"))
    
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    items = relationship("QuoteItem", back_populates="quote")
    orders = relationship("SalesOrder", back_populates="quote")

class QuoteItem(Base):
    __tablename__ = "quote_items"
    
    id = Column(Integer, primary_key=True, index=True)
    quote_id = Column(Integer, ForeignKey("quotes.id"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    description = Column(String(500), nullable=False)
    quantity = Column(Numeric(10, 2), default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(15, 2), nullable=False)
    tax_rate = Column(Numeric(5, 2), default=0)
    tax_amount = Column(Numeric(15, 2), default=0)
    discount_percentage = Column(Numeric(5, 2), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    
    # Relationships
    quote = relationship("Quote", back_populates="items")

class SalesOrder(Base):
    __tablename__ = "sales_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=True)
    
    # Dates
    order_date = Column(DateTime, nullable=False)
    required_date = Column(DateTime)
    shipped_date = Column(DateTime, nullable=True)
    
    # Amounts
    subtotal = Column(Numeric(15, 2), default=0)
    tax_amount = Column(Numeric(15, 2), default=0)
    shipping_cost = Column(Numeric(15, 2), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    total_amount = Column(Numeric(15, 2), default=0)
    
    currency = Column(String(3), default="USD")
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    
    # Shipping info
    shipping_address = Column(Text)
    shipping_city = Column(String(50))
    shipping_state = Column(String(50))
    shipping_country = Column(String(50))
    shipping_postal_code = Column(String(20))
    shipping_method = Column(String(100))
    tracking_number = Column(String(100))
    
    # Additional info
    notes = Column(Text)
    internal_notes = Column(Text)
    
    # Sales rep
    sales_rep_id = Column(Integer, ForeignKey("employees.id"))
    
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    quote = relationship("Quote", back_populates="orders")
    items = relationship("SalesOrderItem", back_populates="order")
    shipments = relationship("Shipment", back_populates="order")

class SalesOrderItem(Base):
    __tablename__ = "sales_order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("sales_orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    description = Column(String(500), nullable=False)
    quantity = Column(Numeric(10, 2), default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(15, 2), nullable=False)
    tax_rate = Column(Numeric(5, 2), default=0)
    tax_amount = Column(Numeric(15, 2), default=0)
    
    # Fulfillment tracking
    quantity_shipped = Column(Numeric(10, 2), default=0)
    quantity_remaining = Column(Numeric(10, 2), default=0)
    
    # Relationships
    order = relationship("SalesOrder", back_populates="items")

class Shipment(Base):
    __tablename__ = "shipments"
    
    id = Column(Integer, primary_key=True, index=True)
    shipment_number = Column(String(50), unique=True, nullable=False)
    order_id = Column(Integer, ForeignKey("sales_orders.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    
    # Dates
    ship_date = Column(DateTime, nullable=False)
    expected_delivery = Column(DateTime)
    actual_delivery = Column(DateTime, nullable=True)
    
    # Shipping details
    carrier = Column(String(100))
    tracking_number = Column(String(100))
    shipping_cost = Column(Numeric(10, 2))
    weight = Column(Numeric(8, 2))
    
    # Address
    shipping_address = Column(Text)
    shipping_city = Column(String(50))
    shipping_state = Column(String(50))
    shipping_country = Column(String(50))
    shipping_postal_code = Column(String(20))
    
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    order = relationship("SalesOrder", back_populates="shipments")
    items = relationship("ShipmentItem", back_populates="shipment")

class ShipmentItem(Base):
    __tablename__ = "shipment_items"
    
    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Numeric(10, 2), nullable=False)
    
    # Relationships
    shipment = relationship("Shipment", back_populates="items")

class SalesTarget(Base):
    __tablename__ = "sales_targets"
    
    id = Column(Integer, primary_key=True, index=True)
    sales_rep_id = Column(Integer, ForeignKey("employees.id"))
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    target_amount = Column(Numeric(15, 2), nullable=False)
    achieved_amount = Column(Numeric(15, 2), default=0)
    currency = Column(String(3), default="USD")
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Commission(Base):
    __tablename__ = "commissions"
    
    id = Column(Integer, primary_key=True, index=True)
    sales_rep_id = Column(Integer, ForeignKey("employees.id"))
    order_id = Column(Integer, ForeignKey("sales_orders.id"))
    commission_rate = Column(Numeric(5, 2), nullable=False)  # Percentage
    commission_amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="USD")
    is_paid = Column(Boolean, default=False)
    paid_date = Column(DateTime, nullable=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=func.now())
