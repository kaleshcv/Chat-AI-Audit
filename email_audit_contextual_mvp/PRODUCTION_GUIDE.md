# Email Audit System - Production Deployment Guide

## Prerequisites
- Python 3.10+
- OpenAI API key

## Installation

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
cp .env.example .env
# Edit .env and fill in:
# - OPENAI_API_KEY (required)
# - DEMO_USERNAME (optional, default: admin)
# - DEMO_PASSWORD (optional, default: admin)
```

### 4. Configuration Files
Ensure these files exist in the project directory:
- `audit_config.json` - Audit configuration and parameters
- `sop_knowledge_base.txt` - SOP knowledge base for auditing

## Running the Application

### Development
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production
```bash
# Using Gunicorn with Uvicorn workers
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

## Security Considerations

### Production Checklist
- [ ] Change default credentials (DEMO_USERNAME, DEMO_PASSWORD)
- [ ] Use environment variables for all sensitive data
- [ ] Enable HTTPS/TLS (Use reverse proxy like Nginx)
- [ ] Implement rate limiting
- [ ] Add database instead of dummy data
- [ ] Use proper authentication (JWT, OAuth2)
- [ ] Implement CORS properly in production
- [ ] Add request logging and monitoring
- [ ] Set secure cookie flags
- [ ] Implement proper error handling
- [ ] Add input validation for all endpoints
- [ ] Use secrets management (e.g., AWS Secrets Manager)

### Cookie Security
Currently using `httponly=True` flag. For production, also add:
```python
response.set_cookie(
    key="logged_in",
    value="true",
    httponly=True,
    secure=True,       # Only send over HTTPS
    samesite="Strict", # Prevent CSRF
    max_age=3600       # 1 hour expiration
)
```

## Logging
Application logs are written to console with INFO level and above.
Levels:
- INFO: Normal operations
- WARNING: Suspicious activities
- ERROR: System errors

## Error Handling
All endpoints include comprehensive error handling and logging.
Errors are logged server-side for debugging.

## API Endpoints

### Authentication
- `GET /` - Redirect to dashboard or login
- `GET /login` - Login page
- `POST /login-submit` - Process login
- `GET /logout` - Logout and clear session

### Dashboard & Audit
- `GET /dashboard` - Management dashboard (requires auth)
- `GET /audit-page` - Audit form (requires auth)
- `POST /audit` - Process audit request (requires auth)

## Performance Optimization
- Enable caching for static responses
- Use connection pooling for OpenAI API
- Implement request queuing for high load
- Monitor API rate limits

## Monitoring
- Set up logging aggregation
- Monitor API error rates
- Track response times
- Alert on failed authentications
- Monitor OpenAI API quota usage

## Troubleshooting

### API Key Error
```
Error: OPENAI_API_KEY environment variable not set
```
Solution: Ensure .env file is created and OPENAI_API_KEY is set.

### Port Already in Use
```bash
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Configuration Files Not Found
Ensure audit_config.json and sop_knowledge_base.txt exist in the project directory.
The application will log warnings if these files are missing.

## Support
For issues or questions, check the application logs for detailed error messages.
