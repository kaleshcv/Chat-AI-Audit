# Email Audit System - Logging Configuration

## Overview
Comprehensive logging has been added throughout the entire application to track all activities, errors, and operations. Logs are written to both console and file for easy monitoring and debugging.

## Logging Features Implemented

### 1. **Enhanced Configuration (config.py)**
- **Log File Location**: `./logs/email_audit.log`
- **Log Level**: Configurable via `LOG_LEVEL` environment variable (default: INFO)
- **Log Format**: Includes timestamp, logger name, level, function name, and line number
- **Rotating File Handler**: Automatic log rotation when file reaches 10MB, keeps last 5 backups
- **Console + File Output**: Logs to both console and file simultaneously

### 2. **Comprehensive Utility Logging (utils.py)**
All utility functions now include detailed logging:

- **load_json_file()**: Logs file load attempts, success, and errors with file size info
- **load_text_file()**: Logs file loading with character count tracking
- **validate_email_thread()**: Logs validation attempts, pass/fail reasons, and thread length
- **safe_json_parse()**: Logs JSON parsing attempts with parsed key counts
- **escape_html()**: Logs HTML escaping operations
- **get_score_color()**: Logs score percentage calculations for color coding

### 3. **Main Application Logging (main.py)**

#### Initialization Logging
- OpenAI client initialization with model and configuration details
- Configuration file loading with section and content counts
- Application startup message with version and log level

#### Authentication Logging
- Login attempts with username tracking
- Login success/failure with detailed reasons
- Credential validation steps
- Session establishment and termination
- Unauthorized access attempts

#### Endpoint Logging
All HTTP endpoints log:
- Request method and path
- Authentication status
- User actions and navigation
- Redirect decisions

**Endpoints with comprehensive logging:**
- GET `/` - Root redirect logic
- GET `/login` - Login page request  
- POST `/login-submit` - Authentication attempts
- GET `/dashboard` - Dashboard access with user auth checks
- GET `/audit-page` - Audit form page access
- GET `/logout` - User logout with session cleanup
- POST `/audit` - Audit request processing

#### Audit Processing Logging
Detailed tracking of the entire audit workflow:
- Audit process initiation
- Input validation with length checks
- Configuration criteria building
- OpenAI API request preparation
- API response handling with token usage tracking
- Result formatting and HTML generation
- Error handling with stack traces

### 4. **Log Levels Used**

| Level | Usage |
|-------|-------|
| **INFO** | Major operations (application start, login, audit completion, important events) |
| **DEBUG** | Detailed diagnostic info (config details, API params, data parsing, function calls) |
| **WARNING** | Unusual events that don't prevent operation (failed login attempts, missing files) |
| **ERROR** | Error conditions that affect operation (API failures, validation errors, exceptions) |

## Log File Details

### Location
```
/Users/Kalesh/ECPL/ChatQA-AI/email_audit_contextual_mvp/logs/email_audit.log
```

### Log Format
```
2024-03-03 14:23:45,123 - email_audit_contextual_mvp.main - INFO - login_submit:456 - Successful login for user: admin
```

Components:
- **Timestamp**: Date and time with milliseconds
- **Logger Name**: Module that generated the log
- **Level**: INFO, DEBUG, WARNING, ERROR
- **Function:Line**: Function name and line number
- **Message**: Detailed log message

### File Rotation
- Maximum file size: 10MB
- Backup files kept: 5
- When full, creates: `email_audit.log.1`, `email_audit.log.2`, etc.

## Environment Variables for Logging

### Configure Log Level
```bash
export LOG_LEVEL=DEBUG    # More detailed logs
export LOG_LEVEL=INFO     # Standard level (default)
export LOG_LEVEL=WARNING  # Only warnings and errors
export LOG_LEVEL=ERROR    # Only errors
```

### Example .env Configuration
```env
# Logging Configuration
LOG_LEVEL=INFO
```

## How to Use Logs

### Monitor Logs in Real-Time
```bash
# Watch console output during application run
tail -f logs/email_audit.log
```

### Search Logs
```bash
# Find all error logs
grep "ERROR" logs/email_audit.log

# Find specific user activity
grep "admin" logs/email_audit.log

# Find API calls
grep "OpenAI" logs/email_audit.log
```

### Analysis Examples
```bash
# Count login attempts
grep "login attempt" logs/email_audit.log | wc -l

# Find all failed operations
grep "ERROR\|WARNING" logs/email_audit.log

# Track specific audit execution
grep "audit_id" logs/email_audit.log
```

## Key Logged Activities

### 1. Authentication Flow
```
User login attempt → Credential validation → Authorization check → Session creation
```

### 2. Audit Execution
```
Audit request received → Input validation → Config loading → 
API request preparation → OpenAI API call → Response parsing → 
Result formatting → HTML generation
```

### 3. Error Handling
```
Error occurrence → Error logging with full stack trace → 
User-friendly error page → Error recovery
```

## Troubleshooting with Logs

### Application Won't Start
Check the startup logs in `logs/email_audit.log` for:
- OpenAI client initialization errors
- Configuration file loading issues
- Directory permission errors

### Login Issues
Search for "login" in logs to see:
- Authentication attempts
- Credential validation failures
- Session-related problems

### Audit Processing Failures
Look for "audit" logs to find:
- Input validation errors
- API request/response issues
- JSON parsing problems
- File I/O errors

## Security Considerations

### What's Logged
- User actions (login/logout)
- API interactions (OpenAI calls)
- Validation activities
- System events

### What's NOT Logged
- Passwords (validation only shows success/failure)
- API keys (only configuration references)
- Sensitive user data (only metadata)

### Log File Security
- Logs are stored in `logs/` directory
- Include full stack traces (be careful in production)
- Review and rotate logs regularly
- Ensure log directory has appropriate permissions

## Performance Impact

Logging has minimal performance impact:
- Asynchronous console output
- Efficient file operations with buffering
- Selective debug logging (disabled by default)
- Log rotation prevents file size issues

## Future Enhancements

Potential logging improvements:
- Structured logging (JSON format)
- Remote log aggregation
- Log analytics dashboard
- Performance metrics tracking
- Request ID tracking across calls
- Custom log handlers for different modules

---

**Last Updated**: March 3, 2026
**Logging System Version**: 1.0
