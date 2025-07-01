"""
Accounting API Routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..core.models import User
from ..modules.accounting.models import Invoice, Customer, Payment, Expense
from .auth import get_current_user

router = APIRouter()

@router.get("/invoices")
async def get_invoices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None
):
    """Get all invoices"""
    query = db.query(Invoice)
    
    if status:
        query = query.filter(Invoice.status == status)
    
    invoices = query.order_by(Invoice.created_at.desc()).offset(skip).limit(limit).all()
    total = query.count()
    
    return {
        "invoices": [
            {
                "id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "customer_id": invoice.customer_id,
                "issue_date": invoice.issue_date,
                "due_date": invoice.due_date,
                "total_amount": float(invoice.total_amount),
                "paid_amount": float(invoice.paid_amount),
                "balance_due": float(invoice.balance_due),
                "status": invoice.status
            }
            for invoice in invoices
        ],
        "total": total
    }

@router.post("/invoices")
async def create_invoice(
    invoice_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new invoice"""
    new_invoice = Invoice(
        invoice_number=invoice_data["invoice_number"],
        customer_id=invoice_data["customer_id"],
        issue_date=invoice_data["issue_date"],
        due_date=invoice_data["due_date"],
        subtotal=invoice_data.get("subtotal", 0),
        tax_amount=invoice_data.get("tax_amount", 0),
        total_amount=invoice_data.get("total_amount", 0),
        balance_due=invoice_data.get("total_amount", 0),
        notes=invoice_data.get("notes"),
        created_by=current_user.id
    )
    
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    
    return {"message": "Invoice created successfully", "invoice_id": new_invoice.id}

@router.get("/customers")
async def get_customers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all customers"""
    customers = db.query(Customer).filter(Customer.is_active == True).offset(skip).limit(limit).all()
    total = db.query(Customer).filter(Customer.is_active == True).count()
    
    return {
        "customers": [
            {
                "id": customer.id,
                "customer_number": customer.customer_number,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone,
                "credit_limit": float(customer.credit_limit) if customer.credit_limit else 0,
                "created_at": customer.created_at
            }
            for customer in customers
        ],
        "total": total
    }

@router.post("/customers")
async def create_customer(
    customer_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new customer"""
    new_customer = Customer(
        customer_number=customer_data.get("customer_number"),
        name=customer_data["name"],
        email=customer_data.get("email"),
        phone=customer_data.get("phone"),
        address=customer_data.get("address"),
        tax_number=customer_data.get("tax_number"),
        credit_limit=customer_data.get("credit_limit"),
        payment_terms=customer_data.get("payment_terms")
    )
    
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    
    return {"message": "Customer created successfully", "customer_id": new_customer.id}

@router.get("/payments")
async def get_payments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all payments"""
    payments = db.query(Payment).order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "payments": [
            {
                "id": payment.id,
                "payment_number": payment.payment_number,
                "invoice_id": payment.invoice_id,
                "amount": float(payment.amount),
                "payment_date": payment.payment_date,
                "payment_method": payment.payment_method,
                "status": payment.status
            }
            for payment in payments
        ]
    }

@router.get("/expenses")
async def get_expenses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get all expenses"""
    expenses = db.query(Expense).order_by(Expense.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "expenses": [
            {
                "id": expense.id,
                "expense_number": expense.expense_number,
                "date": expense.date,
                "vendor": expense.vendor,
                "category": expense.category,
                "description": expense.description,
                "amount": float(expense.amount),
                "is_approved": expense.is_approved
            }
            for expense in expenses
        ]
    }
