# Email Audit System - Production Ready

A FastAPI-based quality assurance system powered by AI for auditing email interactions using OpenAI GPT-4.

## Features

✅ **User Authentication** - Demo login system with configurable credentials  
✅ **Dashboard** - Analytics and insights with dummy data  
✅ **AI-Powered Audits** - Intelligent email thread analysis  
✅ **Configurable Audit Rules** - Flexible parameter definitions via JSON  
✅ **Production Ready** - Logging, error handling, validation, environment config  
✅ **Security** - CORS protection, secure cookies, input validation  

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

1. **Clone and navigate to the project:**
```bash
cd /Users/Kalesh/ECPL/ChatQA-AI/email_audit_contextual_mvp
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables:**
```bash
cp .env.example .env
```

5. **Update `.env` with your settings:**
```env
OPENAI_API_KEY=your-actual-api-key-here
DEMO_USERNAME=admin
DEMO_PASSWORD=admin
APP_DEBUG=false
LOG_LEVEL=INFO
```

## Configuration

### Configuration Files

- **config.py** - Centralized configuration management
- **.env** - Environment variables (create from .env.example)
- **audit_config.json** - Audit parameters and sections
- **sop_knowledge_base.txt** - Standard Operating Procedures

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | (required) | OpenAI API key |
| `DEMO_USERNAME` | admin | Login username |
| `DEMO_PASSWORD` | admin | Login password |
| `APP_DEBUG` | false | Enable debug mode |
| `LOG_LEVEL` | INFO | Logging level |
| `CORS_ORIGINS` | localhost,127.0.0.1 | Allowed origins |

## Running the Application

### Development Mode
```bash
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode
```bash
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Access the application at: `http://localhost:8000`

**Demo Credentials:**
- Username: `admin`
- Password: `admin`

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Redirect to login/dashboard |
| GET | `/login` | Login page |
| POST | `/login-submit` | Process login |
| GET | `/dashboard` | Analytics dashboard |
| GET | `/audit-page` | Audit form page |
| POST | `/audit` | Process audit request |
| GET | `/logout` | Logout and clear session |

## Project Structure

```
email_audit_contextual_mvp/
├── main.py                      # FastAPI application
├── config.py                    # Configuration management
├── utils.py                     # Utility functions
├── audit_config.json           # Audit parameters
├── sop_knowledge_base.txt      # SOP content
├── requirements.txt            # Dependencies
├── .env                        # Environment variables (create from .env.example)
└── README.md                   # This file
```

## Code Modules

### main.py
Main FastAPI application with all endpoints and business logic.

### config.py
Centralized configuration management with environment variables, security settings, and application constants.

### utils.py
Reusable utility functions:
- File loading with error handling
- Input validation
- Safe JSON parsing
- HTML escaping
- Score color determination

## Security Features

🔒 **Implemented Security Measures:**
- Input validation (email thread length limits)
- HTML escaping for safe output
- CORS protection
- Secure HTTP-only cookies
- Session management
- Environment variable management
- Comprehensive logging
- Error handling without exposing sensitive info

## Logging

The application uses Python's built-in logging module. Logs include:
- Application startup
- OpenAI API interactions
- Authentication events
- Audit processing
- Errors and warnings

Log level can be configured via `LOG_LEVEL` environment variable.

## Error Handling

- **Input Validation** - Email threads are validated for length
- **API Errors** - OpenAI API errors are caught and logged
- **File Loading** - Missing files are handled gracefully
- **Authentication** - Unauthorized access is redirected to login
- **JSON Parsing** - Invalid JSON responses are handled safely

## Performance Considerations

- Async request handling via FastAPI
- Efficient file loading with caching (can be added)
- Minimal middleware overhead
- Production-ready CORS configuration

## Deployment

### Using Gunicorn (Recommended for Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Using Docker (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t email-audit .
docker run -p 8000:8000 --env-file .env email-audit
```

## Troubleshooting

**ImportError on startup:**
- Ensure all modules (config.py, utils.py) are in the same directory
- Verify Python path is correct

**OpenAI API errors:**
- Check `OPENAI_API_KEY` is valid
- Verify API key has proper permissions

**Port already in use:**
```bash
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

**Login not working:**
- Check DEMO_USERNAME and DEMO_PASSWORD in .env
- Clear browser cookies

## Development Guidelines

1. **Add logging** to new functions using: `logger.info()`
2. **Validate inputs** using functions from utils.py
3. **Handle exceptions** gracefully with try-except blocks
4. **Use configuration** via config.py constants
5. **Escape HTML** when displaying user input

## License

Proprietary - ECPL

## Support

For issues or questions, contact the development team.
