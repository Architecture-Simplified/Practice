"""
HR API Routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..core.models import User
from ..modules.hr.models import Employee, Department, Attendance, LeaveRequest
from .auth import get_current_user

router = APIRouter()

@router.get("/employees")
async def get_employees(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    department_id: Optional[int] = None
):
    """Get all employees"""
    query = db.query(Employee).filter(Employee.status == "active")
    
    if department_id:
        query = query.filter(Employee.department_id == department_id)
    
    employees = query.offset(skip).limit(limit).all()
    total = query.count()
    
    return {
        "employees": [
            {
                "id": employee.id,
                "employee_id": employee.employee_id,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "email": employee.email,
                "phone": employee.phone,
                "hire_date": employee.hire_date,
                "department_id": employee.department_id,
                "position_id": employee.position_id,
                "status": employee.status
            }
            for employee in employees
        ],
        "total": total
    }

@router.post("/employees")
async def create_employee(
    employee_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new employee"""
    new_employee = Employee(
        employee_id=employee_data["employee_id"],
        first_name=employee_data["first_name"],
        last_name=employee_data["last_name"],
        email=employee_data["email"],
        phone=employee_data.get("phone"),
        date_of_birth=employee_data.get("date_of_birth"),
        hire_date=employee_data["hire_date"],
        department_id=employee_data.get("department_id"),
        position_id=employee_data.get("position_id"),
        salary=employee_data.get("salary"),
        address=employee_data.get("address")
    )
    
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    
    return {"message": "Employee created successfully", "employee_id": new_employee.id}

@router.get("/departments")
async def get_departments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all departments"""
    departments = db.query(Department).filter(Department.is_active == True).all()
    
    return {
        "departments": [
            {
                "id": dept.id,
                "name": dept.name,
                "code": dept.code,
                "description": dept.description,
                "manager_id": dept.manager_id
            }
            for dept in departments
        ]
    }

@router.get("/attendance")
async def get_attendance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    employee_id: Optional[int] = None
):
    """Get attendance records"""
    query = db.query(Attendance)
    
    if employee_id:
        query = query.filter(Attendance.employee_id == employee_id)
    
    records = query.order_by(Attendance.date.desc()).offset(skip).limit(limit).all()
    
    return {
        "attendance": [
            {
                "id": record.id,
                "employee_id": record.employee_id,
                "date": record.date,
                "check_in": record.check_in,
                "check_out": record.check_out,
                "total_hours": float(record.total_hours) if record.total_hours else 0,
                "status": record.status
            }
            for record in records
        ]
    }

@router.get("/leave-requests")
async def get_leave_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None
):
    """Get leave requests"""
    query = db.query(LeaveRequest)
    
    if status:
        query = query.filter(LeaveRequest.status == status)
    
    requests = query.order_by(LeaveRequest.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "leave_requests": [
            {
                "id": request.id,
                "employee_id": request.employee_id,
                "leave_type": request.leave_type,
                "start_date": request.start_date,
                "end_date": request.end_date,
                "days_requested": request.days_requested,
                "reason": request.reason,
                "status": request.status
            }
            for request in requests
        ]
    }
