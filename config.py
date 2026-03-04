"""
Configuration module for Email Audit System
Centralized configuration management for production deployment
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent

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
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Input Validation Limits
MIN_EMAIL_LENGTH = 10
MAX_EMAIL_LENGTH = 50000

# File Paths
CONFIG_FILE = BASE_DIR / "audit_config.json"
SOP_FILE = BASE_DIR / "sop_knowledge_base.txt"

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Validate required configuration
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY not set - some features may not work")
    OPENAI_API_KEY = "sk-default"

logger.info(f"Email Audit System initialized - v{APP_VERSION}")
