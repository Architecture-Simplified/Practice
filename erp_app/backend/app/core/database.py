"""
Database configuration and connection management
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

from .config import settings

# Create database directory if it doesn't exist
os.makedirs("database", exist_ok=True)

# Create SQLAlchemy engine
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(settings.DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Metadata for reflecting tables
metadata = MetaData()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_all_tables():
    """Create all database tables"""
    # Import all models to register them
    from ..modules.crm.models import *
    from ..modules.inventory.models import *
    from ..modules.accounting.models import *
    from ..modules.hr.models import *
    from ..modules.sales.models import *
    
    Base.metadata.create_all(bind=engine)
