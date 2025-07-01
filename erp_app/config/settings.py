"""
Configuration settings for different environments
"""
import os
from typing import List, Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings"""
    
    # Database settings
    database_url: str = "sqlite:///./database/erp_app.db"
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "erp_app"
    database_user: str = "erp_user"
    database_password: str = ""
    
    # JWT settings
    secret_key: str = "your-super-secret-jwt-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Email settings
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    from_email: str = "noreply@yourcompany.com"
    
    # File upload settings
    upload_dir: str = "./uploads"
    max_file_size: int = 10485760  # 10MB
    allowed_extensions: List[str] = [".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx", ".xls", ".xlsx"]
    
    # Redis settings
    redis_url: str = "redis://localhost:6379/0"
    
    # Application settings
    debug: bool = True
    environment: str = "development"
    log_level: str = "INFO"
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Company information
    company_name: str = "Your Company Name"
    company_address: str = "123 Business St, City, State 12345"
    company_phone: str = "+1-555-123-4567"
    company_email: str = "info@yourcompany.com"
    
    # External APIs
    payment_gateway_api_key: str = ""
    shipping_api_key: str = ""
    
    # Backup settings
    backup_enabled: bool = True
    backup_schedule: str = "0 2 * * *"  # Daily at 2 AM
    backup_retention_days: int = 30
    
    @validator('cors_origins', pre=True)
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from environment variable"""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator('allowed_extensions', pre=True)
    def assemble_allowed_extensions(cls, v):
        """Parse allowed extensions from environment variable"""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


class DevelopmentSettings(Settings):
    """Development environment settings"""
    debug: bool = True
    environment: str = "development"
    database_url: str = "sqlite:///./database/erp_app_dev.db"


class ProductionSettings(Settings):
    """Production environment settings"""
    debug: bool = False
    environment: str = "production"
    log_level: str = "WARNING"
    
    # Use PostgreSQL in production
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"


class TestingSettings(Settings):
    """Testing environment settings"""
    debug: bool = True
    environment: str = "testing"
    database_url: str = "sqlite:///:memory:"
    access_token_expire_minutes: int = 5  # Shorter expiry for testing


def get_settings() -> Settings:
    """Get settings based on environment"""
    environment = os.getenv("ENVIRONMENT", "development").lower()
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()


# Global settings instance
settings = get_settings()
