"""
Utility functions for Email Audit System
Common helper functions and utilities
"""

import json
import logging
from pathlib import Path
from typing import Tuple
from html import escape

logger = logging.getLogger(__name__)


def load_json_file(file_path: Path) -> dict:
    """
    Load JSON file safely with error handling.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dictionary from JSON file, or empty dict if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return {}


def load_text_file(file_path: Path) -> str:
    """
    Load text file safely with error handling.
    
    Args:
        file_path: Path to text file
        
    Returns:
        File content as string, or empty string if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return ""
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return ""


def validate_email_thread(email_thread: str, min_length: int = 10, max_length: int = 50000) -> Tuple[bool, str]:
    """
    Validate email thread input.
    
    Args:
        email_thread: Email thread text to validate
        min_length: Minimum required length
        max_length: Maximum allowed length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email_thread:
        return False, "Email thread cannot be empty"
    
    email_thread = email_thread.strip()
    
    if len(email_thread) < min_length:
        return False, f"Email thread is too short (minimum {min_length} characters)"
    
    if len(email_thread) > max_length:
        return False, f"Email thread is too long (maximum {max_length} characters)"
    
    return True, ""


def safe_json_parse(json_str: str) -> dict:
    """
    Safely parse JSON string.
    
    Args:
        json_str: JSON string to parse
        
    Returns:
        Parsed dictionary or empty dict if error
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        return {}


def escape_html(text: str) -> str:
    """
    Escape HTML special characters for safe output.
    
    Args:
        text: Text to escape
        
    Returns:
        Escaped text safe for HTML output
    """
    return escape(text)


def get_score_color(score: float, max_score: float) -> str:
    """
    Determine color class based on score percentage.
    
    Args:
        score: Current score
        max_score: Maximum possible score
        
    Returns:
        CSS class name for color
    """
    if max_score == 0:
        return "score-medium"
    
    percentage = (score / max_score) * 100
    
    if percentage >= 80:
        return "score-high"
    elif percentage >= 50:
        return "score-medium"
    else:
        return "score-low"
