"""
CRM API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
import logging

from ..core.database import get_db
from ..core.models import User
from ..modules.crm.models import Lead, Contact, Deal, Activity
from .auth import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

# Pydantic models for request/response
class LeadCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    status: str = "new"
    source: Optional[str] = None
    notes: Optional[str] = None

class LeadUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    notes: Optional[str] = None

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    notes: Optional[str] = None

class DealCreate(BaseModel):
    title: str
    value: float
    stage: str = "prospecting"
    contact_id: int
    expected_close_date: Optional[datetime] = None
    description: Optional[str] = None

class ActivityCreate(BaseModel):
    title: str
    activity_type: str
    description: Optional[str] = None
    scheduled_at: datetime
    lead_id: Optional[int] = None
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None

@router.get("/leads", status_code=status.HTTP_200_OK)
async def get_leads(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[str] = Query(None, alias="status"),
    company: Optional[str] = None,
    search: Optional[str] = None
):
    """Get all leads with optional filtering and search"""
    try:
        query = db.query(Lead)
        
        # Apply filters
        if status_filter:
            query = query.filter(Lead.status == status_filter)
        
        if company:
            query = query.filter(Lead.company.ilike(f"%{company}%"))
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (Lead.first_name.ilike(search_filter)) |
                (Lead.last_name.ilike(search_filter)) |
                (Lead.email.ilike(search_filter)) |
                (Lead.company.ilike(search_filter))
            )
        
        total = query.count()
        leads = query.offset(skip).limit(limit).all()
        
        logger.info(f"Retrieved {len(leads)} leads for user {current_user.username}")
        
        return {
            "leads": [
                {
                    "id": lead.id,
                    "first_name": lead.first_name,
                    "last_name": lead.last_name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "company": lead.company,
                    "status": lead.status,
                    "source": lead.source,
                    "notes": lead.notes,
                    "created_at": lead.created_at,
                    "updated_at": lead.updated_at
                }
                for lead in leads
            ],
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        logger.error(f"Error retrieving leads: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving leads"
        )

@router.post("/leads", status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead_data: LeadCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new lead"""
    try:
        # Check if lead with same email already exists
        existing_lead = db.query(Lead).filter(Lead.email == lead_data.email).first()
        if existing_lead:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lead with this email already exists"
            )
        
        new_lead = Lead(
            first_name=lead_data.first_name,
            last_name=lead_data.last_name,
            email=lead_data.email,
            phone=lead_data.phone,
            company=lead_data.company,
            status=lead_data.status,
            source=lead_data.source,
            notes=lead_data.notes,
            created_by=current_user.id
        )
        
        db.add(new_lead)
        db.commit()
        db.refresh(new_lead)
        
        logger.info(f"Created new lead {new_lead.id} by user {current_user.username}")
        
        return {
            "id": new_lead.id,
            "first_name": new_lead.first_name,
            "last_name": new_lead.last_name,
            "email": new_lead.email,
            "phone": new_lead.phone,
            "company": new_lead.company,
            "status": new_lead.status,
            "source": new_lead.source,
            "notes": new_lead.notes,
            "created_at": new_lead.created_at
        }
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Database integrity error creating lead: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data integrity error"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating lead: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating lead"
        )

@router.post("/leads")
async def create_lead(
    lead_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new lead"""
    new_lead = Lead(
        first_name=lead_data["first_name"],
        last_name=lead_data["last_name"],
        email=lead_data.get("email"),
        phone=lead_data.get("phone"),
        company=lead_data.get("company"),
        job_title=lead_data.get("job_title"),
        source=lead_data.get("source"),
        notes=lead_data.get("notes"),
        assigned_to=current_user.id
    )
    
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    
    return {"message": "Lead created successfully", "lead_id": new_lead.id}

@router.get("/contacts")
async def get_contacts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all contacts"""
    contacts = db.query(Contact).filter(Contact.is_active == True).offset(skip).limit(limit).all()
    total = db.query(Contact).filter(Contact.is_active == True).count()
    
    return {
        "contacts": [
            {
                "id": contact.id,
                "type": contact.type,
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "company_name": contact.company_name,
                "email": contact.email,
                "phone": contact.phone,
                "created_at": contact.created_at
            }
            for contact in contacts
        ],
        "total": total
    }

@router.post("/contacts")
async def create_contact(
    contact_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new contact"""
    new_contact = Contact(
        type=contact_data.get("type", "individual"),
        first_name=contact_data.get("first_name"),
        last_name=contact_data.get("last_name"),
        company_name=contact_data.get("company_name"),
        email=contact_data.get("email"),
        phone=contact_data.get("phone"),
        website=contact_data.get("website"),
        address=contact_data.get("address"),
        notes=contact_data.get("notes")
    )
    
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    
    return {"message": "Contact created successfully", "contact_id": new_contact.id}

@router.get("/deals")
async def get_deals(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all deals"""
    deals = db.query(Deal).offset(skip).limit(limit).all()
    total = db.query(Deal).count()
    
    return {
        "deals": [
            {
                "id": deal.id,
                "name": deal.name,
                "amount": float(deal.amount) if deal.amount else 0,
                "stage": deal.stage,
                "probability": deal.probability,
                "expected_close_date": deal.expected_close_date,
                "created_at": deal.created_at
            }
            for deal in deals
        ],
        "total": total
    }

@router.post("/deals")
async def create_deal(
    deal_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new deal"""
    new_deal = Deal(
        name=deal_data["name"],
        contact_id=deal_data.get("contact_id"),
        amount=deal_data.get("amount"),
        currency=deal_data.get("currency", "USD"),
        stage=deal_data.get("stage", "prospecting"),
        probability=deal_data.get("probability", 0),
        expected_close_date=deal_data.get("expected_close_date"),
        description=deal_data.get("description"),
        assigned_to=current_user.id
    )
    
    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)
    
    return {"message": "Deal created successfully", "deal_id": new_deal.id}
