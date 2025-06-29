"""
Logging configuration for the project.
"""

import logging
import os
from datetime import datetime

def setup_logging(log_level="INFO"):
    """Set up logging configuration."""
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    log_filename = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)
