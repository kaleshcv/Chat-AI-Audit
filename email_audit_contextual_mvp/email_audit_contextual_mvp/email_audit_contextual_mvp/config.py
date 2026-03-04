"""
Configuration module for Email Audit System
Centralized configuration management for production deployment
"""

import os
import logging
import logging.handlers
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "logs"

# Create logs directory if it doesn't exist
LOGS_DIR.mkdir(exist_ok=True)

# Application Settings
APP_NAME = "Email Audit System"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"

# Security Settings
DEMO_USERNAME = os.getenv("DEMO_USERNAME", "admin")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "admin")
COOKIE_MAX_AGE = 3600  # 1 hour
SESSION_COOKIE_SECURE = not DEBUG  # HTTPS only in production
SESSION_COOKIE_HTTPONLY = True

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_TEMPERATURE = 0.1

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "localhost,127.0.0.1").split(",")
CORS_METHODS = ["GET", "POST"]
CORS_HEADERS = ["*"]

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
LOG_FILE = LOGS_DIR / "email_audit.log"

# Input Validation Limits
MIN_EMAIL_LENGTH = 10
MAX_EMAIL_LENGTH = 50000

# File Paths
CONFIG_FILE = BASE_DIR / "audit_config.json"
SOP_FILE = BASE_DIR / "sop_knowledge_base.txt"

# Setup logging with both file and console handlers
def _setup_logging():
    """Initialize logging configuration with file and console handlers."""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler with rotation
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, LOG_LEVEL))
        file_formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        root_logger.warning(f"Failed to setup file logging: {e}")
    
    return root_logger

# Initialize logging
_setup_logging()
logger = logging.getLogger(__name__)

# Validate required configuration
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY not set - some features may not work")
    OPENAI_API_KEY = "sk-default"

logger.info(f"={' '*60}=")
logger.info(f"Email Audit System initialized - v{APP_VERSION}")
logger.info(f"Debug mode: {DEBUG}")
logger.info(f"Log level: {LOG_LEVEL}")
logger.info(f"Log file: {LOG_FILE}")
logger.info(f"={' '*60}=")
