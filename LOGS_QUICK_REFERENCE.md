# Quick Logging Reference

## View Logs

### Real-time Monitoring
```bash
# Watch logs as they're generated
tail -f /Users/Kalesh/ECPL/ChatQA-AI/email_audit_contextual_mvp/logs/email_audit.log
```

### View Last N Lines
```bash
# Last 50 lines
tail -50 logs/email_audit.log

# Last 100 lines  
tail -100 logs/email_audit.log
```

### Search Logs
```bash
# Find all errors
grep ERROR logs/email_audit.log

# Find specific user activity
grep "admin" logs/email_audit.log

# Find API calls
grep "OpenAI\|API" logs/email_audit.log

# Find login attempts
grep -i "login" logs/email_audit.log

# Find audit operations
grep "audit" logs/email_audit.log
```

## Log Locations

| File | Purpose |
|------|---------|
| `logs/email_audit.log` | Main application log |
| `logs/email_audit.log.1` | Backup 1 (when main exceeds 10MB) |
| `logs/email_audit.log.2` | Backup 2 |
| `logs/email_audit.log.3` | Backup 3 |
| `logs/email_audit.log.4` | Backup 4 |
| `logs/email_audit.log.5` | Backup 5 |

## Common Log Patterns

### Successful Startup
```
Email Audit System initialized - v1.0.0
Debug mode: False
Log level: INFO
Log file: /path/to/logs/email_audit.log
OpenAI client initialized successfully
```

### Successful Login
```
POST /login-submit - Login attempt
Login attempt for username: admin
Validating credentials for user: admin
Credential validation result: success
Successful login for user: admin
```

### Audit Processing
```
POST /audit - Audit request received
Email thread length: 1234 characters
Validating email thread input
Processing audit request
Building audit criteria from configuration
Building audit prompt
Sending audit request to OpenAI API
Using model: gpt-4o-mini, temperature: 0.1
Audit completed successfully
Response length: 4567 characters
Audit completed successfully, formatting results
```

### Error Handling
```
ERROR - Error during audit execution: [error details]
[Full stack trace]
Audit error: [user message]
```

## Setting Log Level

Edit `.env` file:
```env
# For verbose debugging
LOG_LEVEL=DEBUG

# For standard operation
LOG_LEVEL=INFO

# For production (warnings only)
LOG_LEVEL=WARNING
```

Then restart the application.

## Log Analysis Scripts

### Count Activities by Type
```bash
grep -c "ERROR" logs/email_audit.log
grep -c "WARNING" logs/email_audit.log
grep -c "INFO" logs/email_audit.log
grep -c "DEBUG" logs/email_audit.log
```

### Find Issues by Time
```bash
# Logs between specific times
grep "14:2[0-5]" logs/email_audit.log
```

### Track User Activity
```bash
# All activity for a user
grep "admin" logs/email_audit.log | head -20
```

### Monitor Performance
```bash
# Find slow operations (look for timing in logs)
grep "API\|completed" logs/email_audit.log
```

---

**Remember**: Logs rotate automatically when they reach 10MB. Keep last 5 versions as backup.
