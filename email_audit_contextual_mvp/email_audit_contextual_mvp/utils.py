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
    logger.info(f"Loading JSON file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.debug(f"Successfully loaded JSON file with {len(data)} items")
            return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}", exc_info=True)
        return {}


def load_text_file(file_path: Path) -> str:
    """
    Load text file safely with error handling.
    
    Args:
        file_path: Path to text file
        
    Returns:
        File content as string, or empty string if error
    """
    logger.info(f"Loading text file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            logger.debug(f"Successfully loaded text file ({len(content)} characters)")
            return content
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return ""
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}", exc_info=True)
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
    logger.debug(f"Validating email thread: min_length={min_length}, max_length={max_length}")
    
    if not email_thread:
        logger.warning("Validation failed: Email thread is empty")
        return False, "Email thread cannot be empty"
    
    email_thread = email_thread.strip()
    thread_length = len(email_thread)
    
    if thread_length < min_length:
        error_msg = f"Email thread is too short (minimum {min_length} characters, got {thread_length})"
        logger.warning(f"Validation failed: {error_msg}")
        return False, error_msg
    
    if thread_length > max_length:
        error_msg = f"Email thread is too long (maximum {max_length} characters, got {thread_length})"
        logger.warning(f"Validation failed: {error_msg}")
        return False, error_msg
    
    logger.debug(f"Email thread validation passed (length: {thread_length})")
    return True, ""


def safe_json_parse(json_str: str) -> dict:
    """
    Safely parse JSON string.
    
    Args:
        json_str: JSON string to parse
        
    Returns:
        Parsed dictionary or empty dict if error
    """
    logger.debug("Parsing JSON string")
    try:
        data = json.loads(json_str)
        logger.debug(f"Successfully parsed JSON with {len(data)} top-level keys")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}", exc_info=True)
        return {}
    except Exception as e:
        logger.error(f"Unexpected error parsing JSON: {e}", exc_info=True)
        return {}


def escape_html(text: str) -> str:
    """
    Escape HTML special characters for safe output.
    
    Args:
        text: Text to escape
        
    Returns:
        Escaped text safe for HTML output
    """
    logger.debug(f"Escaping HTML text ({len(text)} characters)")
    try:
        escaped = escape(text)
        logger.debug(f"HTML escape completed successfully")
        return escaped
    except Exception as e:
        logger.error(f"Error escaping HTML: {e}", exc_info=True)
        return text


def get_score_color(score: float, max_score: float) -> str:
    """
    Determine color class based on score percentage.
    
    Args:
        score: Current score
        max_score: Maximum possible score
        
    Returns:
        CSS class name for color
    """
    logger.debug(f"Calculating score color: score={score}, max_score={max_score}")
    
    if max_score == 0:
        logger.debug("Max score is 0, returning score-medium")
        return "score-medium"
    
    percentage = (score / max_score) * 100
    logger.debug(f"Score percentage: {percentage:.2f}%")
    
    if percentage >= 80:
        logger.debug("Score percentage >= 80, returning score-high")
        return "score-high"
    elif percentage >= 50:
        logger.debug("Score percentage >= 50, returning score-medium")
        return "score-medium"
    else:
        logger.debug("Score percentage < 50, returning score-low")
        return "score-low"
