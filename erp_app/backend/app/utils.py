"""
Utility functions and helpers for the ERP application
"""
import os
import uuid
import hashlib
from typing import Optional, List, Any, Dict
from datetime import datetime, timedelta
from decimal import Decimal
import re
import mimetypes

from fastapi import UploadFile, HTTPException, status
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import smtplib
import json


class ValidationUtils:
    """Utility class for data validation"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Validate phone number format"""
        pattern = r'^\+?1?-?\.?\s?\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """Validate password strength"""
        result = {
            "is_valid": True,
            "errors": []
        }
        
        if len(password) < 8:
            result["errors"].append("Password must be at least 8 characters long")
        
        if not re.search(r"[A-Z]", password):
            result["errors"].append("Password must contain at least one uppercase letter")
        
        if not re.search(r"[a-z]", password):
            result["errors"].append("Password must contain at least one lowercase letter")
        
        if not re.search(r"\d", password):
            result["errors"].append("Password must contain at least one digit")
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            result["errors"].append("Password must contain at least one special character")
        
        result["is_valid"] = len(result["errors"]) == 0
        return result


class FileUtils:
    """Utility class for file operations"""
    
    @staticmethod
    def generate_filename(original_filename: str) -> str:
        """Generate a unique filename"""
        file_ext = os.path.splitext(original_filename)[1]
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{file_ext}"
    
    @staticmethod
    def validate_file_upload(file: UploadFile, allowed_extensions: List[str], max_size: int) -> bool:
        """Validate uploaded file"""
        # Check file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file_ext} not allowed. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Check file size (this is approximate, actual size check should be done during upload)
        if hasattr(file, 'size') and file.size > max_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum allowed size of {max_size} bytes"
            )
        
        return True
    
    @staticmethod
    def get_file_hash(file_path: str) -> str:
        """Generate SHA256 hash of a file"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()


class DateUtils:
    """Utility class for date operations"""
    
    @staticmethod
    def get_current_datetime() -> datetime:
        """Get current datetime"""
        return datetime.utcnow()
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format datetime to string"""
        return dt.strftime(format_str)
    
    @staticmethod
    def parse_datetime(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
        """Parse string to datetime"""
        return datetime.strptime(date_str, format_str)
    
    @staticmethod
    def get_date_range(start_date: datetime, end_date: datetime) -> List[datetime]:
        """Generate list of dates between start and end date"""
        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date)
            current_date += timedelta(days=1)
        return dates


class CurrencyUtils:
    """Utility class for currency operations"""
    
    @staticmethod
    def format_currency(amount: Decimal, currency: str = "USD") -> str:
        """Format amount as currency"""
        return f"{currency} {amount:,.2f}"
    
    @staticmethod
    def calculate_tax(amount: Decimal, tax_rate: Decimal) -> Decimal:
        """Calculate tax amount"""
        return amount * (tax_rate / 100)
    
    @staticmethod
    def calculate_discount(amount: Decimal, discount_percent: Decimal) -> Decimal:
        """Calculate discount amount"""
        return amount * (discount_percent / 100)


class EmailUtils:
    """Utility class for email operations"""
    
    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        body: str,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        from_email: str,
        is_html: bool = False
    ) -> bool:
        """Send email"""
        try:
            msg = MimeMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg_body = MimeText(body, 'html' if is_html else 'plain')
            msg.attach(msg_body)
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False


class DataUtils:
    """Utility class for data operations"""
    
    @staticmethod
    def serialize_datetime(obj: Any) -> str:
        """Serialize datetime objects for JSON"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    @staticmethod
    def clean_string(text: str) -> str:
        """Clean and normalize string"""
        return text.strip().title() if text else ""
    
    @staticmethod
    def generate_unique_code(prefix: str = "", length: int = 8) -> str:
        """Generate unique code"""
        unique_part = str(uuid.uuid4()).replace('-', '')[:length]
        return f"{prefix}{unique_part}".upper()
    
    @staticmethod
    def paginate_results(query, page: int, per_page: int):
        """Paginate database query results"""
        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }


class SecurityUtils:
    """Utility class for security operations"""
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input to prevent XSS"""
        if not text:
            return ""
        
        # Remove potential script tags and dangerous characters
        text = re.sub(r'<script.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    @staticmethod
    def mask_sensitive_data(data: str, mask_char: str = '*', visible_chars: int = 4) -> str:
        """Mask sensitive data like credit card numbers"""
        if len(data) <= visible_chars:
            return mask_char * len(data)
        
        masked_part = mask_char * (len(data) - visible_chars)
        visible_part = data[-visible_chars:]
        return masked_part + visible_part
