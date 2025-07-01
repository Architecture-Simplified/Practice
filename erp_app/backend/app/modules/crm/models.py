"""
CRM (Customer Relationship Management) Models
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime

from ...core.database import Base

class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    LOST = "lost"

class ContactType(str, enum.Enum):
    INDIVIDUAL = "individual"
    COMPANY = "company"

class DealStage(str, enum.Enum):
    PROSPECTING = "prospecting"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20))
    company = Column(String(100))
    job_title = Column(String(100))
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    source = Column(String(50))  # Website, Referral, Cold Call, etc.
    notes = Column(Text)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    activities = relationship("Activity", back_populates="lead")

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(ContactType), default=ContactType.INDIVIDUAL)
    first_name = Column(String(50))
    last_name = Column(String(50))
    company_name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20))
    mobile = Column(String(20))
    website = Column(String(200))
    address = Column(Text)
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    postal_code = Column(String(20))
    job_title = Column(String(100))
    department = Column(String(100))
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    deals = relationship("Deal", back_populates="contact")
    activities = relationship("Activity", back_populates="contact")

class Deal(Base):
    __tablename__ = "deals"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    amount = Column(Numeric(15, 2))
    currency = Column(String(3), default="USD")
    stage = Column(Enum(DealStage), default=DealStage.PROSPECTING)
    probability = Column(Integer, default=0)  # 0-100%
    expected_close_date = Column(DateTime)
    description = Column(Text)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    contact = relationship("Contact", back_populates="deals")
    activities = relationship("Activity", back_populates="deal")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50))  # call, email, meeting, note, task
    subject = Column(String(200), nullable=False)
    description = Column(Text)
    scheduled_at = Column(DateTime)
    completed_at = Column(DateTime)
    is_completed = Column(Boolean, default=False)
    
    # Related entities (one of these will be set)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=True)
    
    assigned_to = Column(Integer, ForeignKey("users.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    lead = relationship("Lead", back_populates="activities")
    contact = relationship("Contact", back_populates="activities")
    deal = relationship("Deal", back_populates="activities")
