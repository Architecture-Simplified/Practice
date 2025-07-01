"""
Database initialization script
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.database import Base, engine, SessionLocal
from app.core.models import User, SystemSetting
from app.core.security import get_password_hash
from app.modules.crm.models import Lead, Contact, Deal
from app.modules.inventory.models import Product, Category, Warehouse
from app.modules.accounting.models import Customer, Invoice
from app.modules.hr.models import Employee, Department
from app.modules.sales.models import Quote, SalesOrder

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

def create_admin_user():
    """Create default admin user"""
    print("Creating admin user...")
    
    db = SessionLocal()
    
    try:
        # Check if admin user exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@erp.com",
                full_name="System Administrator",
                hashed_password=get_password_hash("admin123"),
                role="super_admin",
                is_active=True,
                is_verified=True
            )
            
            db.add(admin_user)
            db.commit()
            print("Admin user created successfully!")
            print("Username: admin")
            print("Email: admin@erp.com")
            print("Password: admin123")
        else:
            print("Admin user already exists!")
            
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_data():
    """Create sample data for demonstration"""
    print("Creating sample data...")
    
    db = SessionLocal()
    
    try:
        # Sample Categories
        if not db.query(Category).first():
            categories = [
                Category(name="Electronics", description="Electronic products"),
                Category(name="Software", description="Software products"),
                Category(name="Services", description="Service offerings")
            ]
            db.add_all(categories)
        
        # Sample Customers
        if not db.query(Customer).first():
            customers = [
                Customer(
                    customer_number="CUST001",
                    name="Acme Corporation",
                    email="contact@acme.com",
                    phone="+1-555-0123",
                    address="123 Business St"
                ),
                Customer(
                    customer_number="CUST002",
                    name="Tech Solutions Inc",
                    email="info@techsolutions.com",
                    phone="+1-555-0124",
                    address="456 Tech Ave"
                )
            ]
            db.add_all(customers)
        
        # Sample Departments
        if not db.query(Department).first():
            departments = [
                Department(name="Information Technology", code="IT"),
                Department(name="Sales", code="SALES"),
                Department(name="Human Resources", code="HR"),
                Department(name="Finance", code="FIN")
            ]
            db.add_all(departments)
        
        # Sample Warehouse
        if not db.query(Warehouse).first():
            warehouse = Warehouse(
                name="Main Warehouse",
                code="WH001",
                address="789 Warehouse Blvd",
                city="Business City",
                manager_name="John Manager"
            )
            db.add(warehouse)
        
        db.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

def create_system_settings():
    """Create default system settings"""
    print("Creating system settings...")
    
    db = SessionLocal()
    
    try:
        settings = [
            SystemSetting(
                key="company_name",
                value="ERP Demo Company",
                description="Company name for the ERP system"
            ),
            SystemSetting(
                key="company_address",
                value="123 Business Street, City, Country",
                description="Company address"
            ),
            SystemSetting(
                key="currency",
                value="USD",
                description="Default currency"
            ),
            SystemSetting(
                key="timezone",
                value="UTC",
                description="Default timezone"
            )
        ]
        
        for setting in settings:
            existing = db.query(SystemSetting).filter(SystemSetting.key == setting.key).first()
            if not existing:
                db.add(setting)
        
        db.commit()
        print("System settings created successfully!")
        
    except Exception as e:
        print(f"Error creating system settings: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main initialization function"""
    print("=== ERP System Database Initialization ===")
    
    try:
        create_tables()
        create_admin_user()
        create_sample_data()
        create_system_settings()
        
        print("\n=== Initialization Complete ===")
        print("You can now start the application with: python backend/main.py")
        print("Default login: admin@erp.com / admin123")
        
    except Exception as e:
        print(f"Initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
