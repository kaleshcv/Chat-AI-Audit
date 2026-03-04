# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Prerequisites
- Python 3.8+ installed
- Command line/Terminal access

### Step 1: Navigate to Project
```bash
cd /Users/Kalesh/ECPL/ChatQA-AI/email_audit_contextual_mvp
```

### Step 2: Activate Virtual Environment
```bash
source /Users/Kalesh/ECPL/ChatQA-AI/venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API Key
# OPENAI_API_KEY=sk-your-key-here
```

### Step 5: Run the Application
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 6: Access the Application
Open your browser and go to:
```
http://localhost:8000
```

## 📋 Login Credentials (Demo)
- **Username:** admin
- **Password:** admin

## 🎯 What to Do

1. **Log in** with the demo credentials
2. **View Dashboard** - See analytics and metrics
3. **Run New Audit** - Paste an email thread and run an audit
4. **View Results** - See detailed audit results with scores

## 📁 Project Structure

```
email_audit_contextual_mvp/
├── main.py                    # FastAPI application
├── config.py                  # Configuration settings
├── utils.py                   # Utility functions
├── audit_config.json         # Audit parameters
├── sop_knowledge_base.txt    # SOP content
├── requirements.txt          # Dependencies
├── .env                      # Environment variables (create from .env.example)
├── README_PRODUCTION.md      # Full documentation
├── DEPLOYMENT_CHECKLIST.md   # Deployment guide
└── PRODUCTION_OPTIMIZATIONS.md  # Optimization details
```

## 🔑 Important Files

| File | Purpose |
|------|---------|
| `main.py` | Main FastAPI application with all endpoints |
| `config.py` | Configuration management and environment variables |
| `utils.py` | Reusable utility functions |
| `.env` | Secret API keys and credentials (create from .env.example) |

## 🛑 Stop the Application

Press `Ctrl+C` in the terminal running the server.

## 🐛 Troubleshooting

**Port 8000 already in use?**
```bash
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

**Missing dependencies?**
```bash
pip install -r requirements.txt
```

**OpenAI API key not working?**
1. Check .env file has correct API key
2. Verify API key is valid at https://platform.openai.com/account/api-keys
3. Check your OpenAI account has available credits

**Can't log in?**
1. Make sure you're using: `admin` / `admin`
2. Check .env file for DEMO_USERNAME and DEMO_PASSWORD
3. Clear browser cookies and try again

## 📖 Next Steps

1. Read **README_PRODUCTION.md** for full documentation
2. Check **PRODUCTION_OPTIMIZATIONS.md** for technical details
3. Review **DEPLOYMENT_CHECKLIST.md** for production deployment
4. Look at **config.py** to understand configuration options
5. Check **utils.py** for available utility functions

## 🔐 Security Note

⚠️ **Important:** The .env.example file shows a dummy API key. Replace it with your actual OpenAI API key before deployment.

Never commit .env file to version control!

## 💡 Tips

- The dashboard has dummy data for demonstration
- You can modify audit_config.json to change audit parameters
- Edit sop_knowledge_base.txt to update the SOP content
- Logs are output to the console during development

## 📞 Support

For detailed information, see:
- `README_PRODUCTION.md` - Full documentation
- `PRODUCTION_OPTIMIZATIONS.md` - Architecture and optimizations
- `DEPLOYMENT_CHECKLIST.md` - Deployment procedures

---

**Happy Auditing! 🎉**
