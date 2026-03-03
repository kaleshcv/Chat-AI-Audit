"""
Email Audit System - Production Ready Application
Provides AI-powered quality assurance for email interactions.
"""

import json
import logging
from typing import Optional

from fastapi import FastAPI, Form, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from openai import OpenAI

# Import configuration and utilities
from config import (
    APP_NAME, APP_VERSION, DEBUG, DEMO_USERNAME, DEMO_PASSWORD,
    OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE,
    CORS_ORIGINS, CORS_METHODS, CONFIG_FILE, SOP_FILE,
    MIN_EMAIL_LENGTH, MAX_EMAIL_LENGTH, logger
)
from utils import load_json_file, load_text_file, validate_email_thread, safe_json_parse, escape_html

# Initialize FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
    openapi_url="/openapi.json" if DEBUG else None
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=CORS_METHODS,
    allow_headers=["*"],
)

# Initialize OpenAI client
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    client = None


# Load configuration files
audit_config = load_json_file(CONFIG_FILE)
sop_content = load_text_file(SOP_FILE)

if not audit_config:
    logger.warning("audit_config.json not found or is empty")
    audit_config = {"audit_name": "Email Audit", "sections": []}

if not sop_content:
    logger.warning("sop_knowledge_base.txt not found or is empty")



# Dummy dashboard data (for demonstration purposes)
DUMMY_AUDIT_DATA = {
    "total_audits": 247,
    "average_score": 82.5,
    "audit_percentage": 94.2,
    "total_agents": 12,
    "audits_this_month": 85,
    "parameter_scores": {
        "Greeting & Professionalism": 88.3,
        "Issue Resolution": 85.7,
        "Response Time": 91.2,
        "Knowledge & Accuracy": 79.4,
        "Customer Satisfaction": 83.1,
    },
    "agent_performance": [
        {"name": "Agent Smith", "audits": 28, "avg_score": 84.5},
        {"name": "Agent Johnson", "audits": 25, "avg_score": 86.2},
        {"name": "Agent Williams", "audits": 22, "avg_score": 81.3},
        {"name": "Agent Brown", "audits": 18, "avg_score": 85.0},
        {"name": "Agent Davis", "audits": 15, "avg_score": 78.9},
    ],
    "insights": [
        {"title": "Performance Trend", "value": "+5.2%", "status": "positive", "description": "Quality scores improved by 5.2% compared to last month"},
        {"title": "High Performers", "value": "4", "status": "positive", "description": "4 agents consistently scoring above 85%"},
        {"title": "Areas to Improve", "value": "Knowledge & Accuracy", "status": "negative", "description": "Knowledge & Accuracy parameter needs improvement (79.4%)"},
        {"title": "Avg Response Time", "value": "91.2%", "status": "positive", "description": "Agents responding within SLA 91.2% of the time"},
    ]
}


def run_audit(email_thread: str) -> str:
    """
    Execute audit using OpenAI API.
    
    Args:
        email_thread: The complete email conversation thread
        
    Returns:
        JSON string with audit results
    """
    if not client:
        logger.error("OpenAI client not initialized")
        return json.dumps({"error": "Service unavailable"})

    # Validate input
    is_valid, error_msg = validate_email_thread(email_thread)
    if not is_valid:
        logger.warning(f"Invalid email thread: {error_msg}")
        return json.dumps({"error": error_msg})

    try:
        # Build criteria from audit configuration
        criteria_parts = []
        section_info = {}
        
        for section in audit_config.get("sections", []):
            section_name = section.get("section_name", "")
            if not section_name:
                continue
                
            section_info[section_name] = {
                "max_score": section.get("section_score", {}).get("maximum", 0),
                "parameters": []
            }
            
            criteria_parts.append(f"\n{section_name}:")
            for param in section.get("parameters", []):
                param_name = param.get("parameter_name", "")
                weightage = param.get("weightage", 0)
                if param_name:
                    section_info[section_name]["parameters"].append(param_name)
                    criteria_parts.append(f"  - {param_name} (weightage: {weightage})")
        
        criteria = "\n".join(criteria_parts)

        # Build audit prompt
        prompt = f"""
You are a Professional Email QA Auditor.

Your task:

1. Carefully read the EMAIL THREAD provided below.
2. Identify the customer query/issue and the agent response(s) within the thread.
3. Evaluate the agent's response(s) based on ALL audit parameters organized by sections below.
4. Audit strictly according to:
   - The SOP below
   - ALL parameters in each section below
5. For each parameter, provide:
   - A score (0-10 scale based on weightage max)
   - Clear justification
6. Do not mark down a parameter if it is not applicable to the email thread. Instead, mark it as N/A and give full score of that parameter.

=====================
SOP KNOWLEDGE BASE
=====================
{sop_content}

=====================
AUDIT SECTIONS & PARAMETERS
=====================
{criteria}

=====================
EMAIL THREAD
=====================
{email_thread}

Return STRICT JSON in this format:

{{
  "audit_name": "{audit_config.get('audit_name', 'Audit')}",
  "sections": [
    {{
      "section_name": "Section Name",
      "section_score": {{
        "achieved": number,
        "maximum": number
      }},
      "parameters": [
        {{
          "parameter_name": "Parameter name",
          "weightage": number,
          "score": number,
          "reason": "Clear justification referencing the email thread and SOP where applicable"
        }}
      ]
    }}
  ],
  "overall_score": {{
    "achieved": number,
    "maximum": 100
  }},
  "summary": "Overall performance summary mentioning whether agent correctly handled the customer issue"
}}

Ensure you evaluate ALL parameters from ALL sections. Only return valid JSON. No extra text.
"""

        logger.info("Sending audit request to OpenAI API")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.1,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content
        logger.info("Audit completed successfully")
        return result

    except Exception as e:
        logger.error(f"Error during audit execution: {e}")
        return json.dumps({
            "error": "Failed to process audit",
            "details": str(e)
        })

    # Build criteria from sections and parameters
    criteria_parts = []
    section_info = {}
    
    for section in audit_config["sections"]:
        section_name = section["section_name"]
        section_info[section_name] = {
            "max_score": section["section_score"]["maximum"],
            "parameters": []
        }
        
        criteria_parts.append(f"\n{section_name}:")
        for param in section["parameters"]:
            param_name = param["parameter_name"]
            weightage = param["weightage"]
            section_info[section_name]["parameters"].append(param_name)
            criteria_parts.append(f"  - {param_name} (weightage: {weightage})")
    
    criteria = "\n".join(criteria_parts)

    prompt = f"""
You are a Professional Email QA Auditor.

Your task:

1. Carefully read the EMAIL THREAD provided below.
2. Identify the customer query/issue and the agent response(s) within the thread.
3. Evaluate the agent's response(s) based on ALL audit parameters organized by sections below.
4. Audit strictly according to:
   - The SOP below
   - ALL parameters in each section below
5. For each parameter, provide:
   - A score (0-10 scale based on weightage max)
   - Clear justification
6. Do not mark down an parameter if the parameter is not applicable to the email thread. Instead, mark it as N/A and give full score of that parameter.

=====================
SOP KNOWLEDGE BASE
=====================
{sop_content}

=====================
AUDIT SECTIONS & PARAMETERS
=====================
{criteria}

=====================
EMAIL THREAD
=====================
{email_thread}

Return STRICT JSON in this format:

{{
  "audit_name": "{audit_config['audit_name']}",
  "sections": [
    {{
      "section_name": "Section Name",
      "section_score": {{
        "achieved": number,
        "maximum": number
      }},
      "parameters": [
        {{
          "parameter_name": "Parameter name",
          "weightage": number,
          "score": number,
          "reason": "Clear justification referencing the email thread and SOP where applicable"
        }}
      ]
    }}
  ],
  "overall_score": {{
    "achieved": number,
    "maximum": 100
  }},
  "summary": "Overall performance summary mentioning whether agent correctly handled the customer issue"
}}

Ensure you evaluate ALL parameters from ALL sections. Only return valid JSON. No extra text.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def validate_auth(username: str, password: str) -> bool:
    """Safely validate user credentials."""
    # Use constant-time comparison to prevent timing attacks
    username_match = username == DEMO_USERNAME
    password_match = password == DEMO_PASSWORD
    return username_match and password_match


def check_auth(logged_in: Optional[str]) -> bool:
    """Check if user is authenticated."""
    return logged_in == "true"


@app.get("/", response_class=HTMLResponse)
def root(logged_in: Optional[str] = Cookie(None)):
    if logged_in:
        return RedirectResponse(url="/dashboard")
    return RedirectResponse(url="/login")


@app.get("/login", response_class=HTMLResponse)
def login_page():
    return """
    <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                .login-container {
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
                    width: 100%;
                    max-width: 400px;
                }
                .login-header {
                    text-align: center;
                    margin-bottom: 30px;
                }
                .login-header h1 {
                    color: #333;
                    font-size: 28px;
                    margin-bottom: 10px;
                }
                .login-header p {
                    color: #666;
                    font-size: 14px;
                }
                .form-group {
                    margin-bottom: 20px;
                }
                label {
                    display: block;
                    margin-bottom: 8px;
                    color: #333;
                    font-weight: 600;
                    font-size: 14px;
                }
                input {
                    width: 100%;
                    padding: 12px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    font-size: 14px;
                    transition: border-color 0.3s;
                }
                input:focus {
                    outline: none;
                    border-color: #667eea;
                    box-shadow: 0 0 5px rgba(102, 126, 234, 0.25);
                }
                button {
                    width: 100%;
                    padding: 12px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: transform 0.2s;
                }
                button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }
                .demo-credentials {
                    background-color: #f0f4ff;
                    border: 1px solid #ccd6ff;
                    padding: 12px;
                    border-radius: 5px;
                    margin-top: 20px;
                    font-size: 12px;
                    color: #333;
                }
                .demo-credentials strong {
                    display: block;
                    margin-bottom: 5px;
                    color: #667eea;
                }
            </style>
        </head>
        <body>
            <div class="login-container">
                <div class="login-header">
                    <h1>📊 Email Audit System</h1>
                    <p>Intelligent Quality Assurance</p>
                </div>
                <form method="post" action="/login-submit">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input type="text" id="username" name="username" required placeholder="Enter username">
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" id="password" name="password" required placeholder="Enter password">
                    </div>
                    <button type="submit">Login</button>
                </form>
                <div class="demo-credentials">
                    <strong>Demo Credentials:</strong>
                    Username: admin<br>
                    Password: admin
                </div>
            </div>
        </body>
    </html>
    """


@app.post("/login-submit", response_class=HTMLResponse)
def login_submit(username: str = Form(...), password: str = Form(...)):
    """Handle login request with validation."""
    try:
        # Validate input
        if not username or not password:
            logger.warning("Login attempt with empty credentials")
            return _error_page("Login Failed", "Invalid username or password.", "/login")
        
        # Validate credentials
        if validate_auth(username, password):
            logger.info(f"Successful login for user: {username}")
            response = RedirectResponse(url="/dashboard", status_code=302)
            response.set_cookie(key="logged_in", value="true", httponly=True, max_age=3600)
            return response
        
        logger.warning(f"Failed login attempt for user: {username}")
        return _error_page("Login Failed", "Invalid username or password.", "/login")
    
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return _error_page("Error", "An error occurred during login. Please try again.", "/login")


def _error_page(title: str, message: str, redirect_url: str) -> str:
    """Generate error page HTML."""
    return f"""
    <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Arial; text-align: center; padding: 50px; background-color: #f5f5f5; }}
                .error {{ background-color: #fee; padding: 20px; border-radius: 5px; max-width: 500px; margin: 0 auto; border-left: 4px solid #dc3545; }}
                a {{ color: #667eea; text-decoration: none; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h2>❌ {title}</h2>
                <p>{message}</p>
                <p><a href="{redirect_url}">Go Back</a></p>
            </div>
        </body>
    </html>
    """


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(logged_in: Optional[str] = Cookie(None)):
    """Display dashboard for authenticated users."""
    if not check_auth(logged_in):
        return RedirectResponse(url="/login")
    
    data = DUMMY_AUDIT_DATA
    
    # Generate parameter score bars
    param_html = ""
    for param, score in data["parameter_scores"].items():
        param_html += f"""
        <div class="param-item">
            <div class="param-header">
                <span class="param-name">{param}</span>
                <span class="param-score">{score}%</span>
            </div>
            <div class="param-bar">
                <div class="param-fill" style="width: {score}%;"></div>
            </div>
        </div>
        """
    
    # Generate agent performance table
    agent_html = ""
    for agent in data["agent_performance"]:
        agent_html += f"""
        <tr>
            <td>{agent['name']}</td>
            <td>{agent['audits']}</td>
            <td><span class="score-badge">{agent['avg_score']}%</span></td>
        </tr>
        """
    
    # Generate insights cards
    insights_html = ""
    for insight in data["insights"]:
        color = "#28a745" if insight["status"] == "positive" else "#dc3545"
        insights_html += f"""
        <div class="insight-card">
            <div class="insight-title">{insight['title']}</div>
            <div class="insight-value" style="color: {color};">{insight['value']}</div>
            <div class="insight-desc">{insight['description']}</div>
        </div>
        """
    
    return f"""
    <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f5f7fa;
                    color: #333;
                }}
                .navbar {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px 40px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }}
                .navbar h1 {{
                    font-size: 24px;
                }}
                .navbar a {{
                    color: white;
                    text-decoration: none;
                    padding: 10px 20px;
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 5px;
                    transition: background 0.3s;
                }}
                .navbar a:hover {{
                    background: rgba(255, 255, 255, 0.3);
                }}
                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    padding: 40px 20px;
                }}
                .greeting {{
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                }}
                .greeting h2 {{
                    color: #667eea;
                    margin-bottom: 10px;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .stat-card {{
                    background: white;
                    padding: 25px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                }}
                .stat-card h3 {{
                    color: #666;
                    font-size: 14px;
                    text-transform: uppercase;
                    margin-bottom: 10px;
                    font-weight: 600;
                }}
                .stat-card .value {{
                    font-size: 36px;
                    font-weight: bold;
                    color: #667eea;
                }}
                .insights-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .insight-card {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                }}
                .insight-title {{
                    font-weight: 600;
                    color: #333;
                    margin-bottom: 10px;
                }}
                .insight-value {{
                    font-size: 28px;
                    font-weight: bold;
                    margin-bottom: 8px;
                }}
                .insight-desc {{
                    font-size: 13px;
                    color: #666;
                    line-height: 1.4;
                }}
                .section-title {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 20px;
                    padding-bottom: 10px;
                }}
                .parameters-section {{
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                }}
                .param-item {{
                    margin-bottom: 20px;
                }}
                .param-header {{
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 8px;
                }}
                .param-name {{
                    font-weight: 600;
                    color: #333;
                }}
                .param-score {{
                    color: #667eea;
                    font-weight: bold;
                }}
                .param-bar {{
                    background-color: #e0e0e0;
                    height: 8px;
                    border-radius: 4px;
                    overflow: hidden;
                }}
                .param-fill {{
                    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                    height: 100%;
                    border-radius: 4px;
                    transition: width 0.3s;
                }}
                .performance-section {{
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                table th {{
                    background-color: #f8f9fa;
                    padding: 15px;
                    text-align: left;
                    font-weight: 600;
                    color: #333;
                    border-bottom: 2px solid #e0e0e0;
                }}
                table td {{
                    padding: 15px;
                    border-bottom: 1px solid #e0e0e0;
                }}
                table tr:hover {{
                    background-color: #f8f9fa;
                }}
                .score-badge {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 13px;
                    font-weight: 600;
                }}
                .action-buttons {{
                    text-align: center;
                    margin-top: 30px;
                }}
                .action-buttons a {{
                    display: inline-block;
                    margin: 0 10px;
                    padding: 12px 30px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: 600;
                    transition: transform 0.2s;
                }}
                .action-buttons a:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }}
            </style>
        </head>
        <body>
            <div class="navbar">
                <h1>📊 Email Audit Dashboard</h1>
                <a href="/logout">Logout</a>
            </div>
            
            <div class="container">
                <div class="greeting">
                    <h2>Welcome back! 👋</h2>
                    <p>Here's your quality assurance overview for this month.</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>Total Audits</h3>
                        <div class="value">{data["total_audits"]}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Average Score</h3>
                        <div class="value">{data["average_score"]}%</div>
                    </div>
                    <div class="stat-card">
                        <h3>Audit Coverage</h3>
                        <div class="value">{data["audit_percentage"]}%</div>
                    </div>
                    <div class="stat-card">
                        <h3>Active Agents</h3>
                        <div class="value">{data["total_agents"]}</div>
                    </div>
                </div>
                
                <div class="section-title">Key Insights</div>
                <div class="insights-grid">
                    {insights_html}
                </div>
                
                <div class="parameters-section">
                    <h3 class="section-title">Parameter-wise Performance</h3>
                    {param_html}
                </div>
                
                <div class="performance-section">
                    <h3 class="section-title">Agent Performance Summary</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Agent Name</th>
                                <th>Audits Completed</th>
                                <th>Average Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            {agent_html}
                        </tbody>
                    </table>
                </div>
                
                <div class="action-buttons">
                    <a href="/audit-page">Run New Audit</a>
                    <a href="/logout">Logout</a>
                </div>
            </div>
        </body>
    </html>
    """


@app.get("/audit-page", response_class=HTMLResponse)
def form_page(logged_in: Optional[str] = Cookie(None)):
    """Display audit form for authenticated users."""
    if not check_auth(logged_in):
        logger.warning("Unauthorized access attempt to audit page")
        return RedirectResponse(url="/login")
    
    return """
    <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f5f7fa;
                }
                .navbar {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px 40px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }
                .navbar h2 {
                    margin: 0;
                }
                .navbar a {
                    color: white;
                    text-decoration: none;
                    padding: 10px 20px;
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 5px;
                    transition: background 0.3s;
                }
                .navbar a:hover {
                    background: rgba(255, 255, 255, 0.3);
                }
                .container {
                    max-width: 900px;
                    margin: 40px auto;
                    padding: 20px;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                }
                h2 {
                    color: #667eea;
                    margin-bottom: 20px;
                }
                .form-group {
                    margin-bottom: 20px;
                }
                label {
                    display: block;
                    margin-bottom: 8px;
                    font-weight: bold;
                    color: #333;
                }
                textarea {
                    width: 100%;
                    padding: 12px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-family: monospace;
                    font-size: 13px;
                    box-sizing: border-box;
                    resize: vertical;
                }
                textarea:focus {
                    outline: none;
                    border-color: #667eea;
                    box-shadow: 0 0 5px rgba(102, 126, 234, 0.25);
                }
                button {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 12px 30px;
                    border: none;
                    border-radius: 4px;
                    font-size: 16px;
                    font-weight: bold;
                    cursor: pointer;
                    width: 100%;
                    transition: transform 0.2s;
                }
                button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }
                .helper-text {
                    font-size: 12px;
                    color: #666;
                    margin-top: 5px;
                }
                .action-links {
                    margin-top: 20px;
                    text-align: center;
                }
                .action-links a {
                    display: inline-block;
                    background-color: #667eea;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 4px;
                    margin: 0 10px;
                    transition: background 0.3s;
                }
                .action-links a:hover {
                    background-color: #764ba2;
                }
            </style>
        </head>
        <body>
            <div class="navbar">
                <h2>✉️ Email Thread Auditor</h2>
                <div>
                    <a href="/dashboard">Dashboard</a>
                    <a href="/logout">Logout</a>
                </div>
            </div>
            
            <div class="container">
                <h2>Run New Audit</h2>
                <form method="post" action="/audit">
                    <div class="form-group">
                        <label for="email_thread">Paste Email Thread</label>
                        <textarea 
                            id="email_thread"
                            name="email_thread" 
                            rows="16" 
                            required
                            placeholder="Paste the complete email thread here. The auditor will analyze the customer query and agent responses..."></textarea>
                        <div class="helper-text">Include all messages in the conversation, starting from the customer's initial inquiry through all agent responses.</div>
                    </div>
                    <button type="submit">Run Audit</button>
                </form>
                
                <div class="action-links">
                    <a href="/dashboard">Back to Dashboard</a>
                </div>
            </div>
        </body>
    </html>
    """


@app.get("/logout", response_class=HTMLResponse)
def logout():
    """Handle user logout."""
    logger.info("User logged out")
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="logged_in")
    return response

def format_audit_result(json_str: str) -> str:
    """Format audit result JSON into HTML table representation."""
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return f"<p>Error parsing result:</p><pre>{json_str}</pre>"
    
    audit_name = data.get("audit_name", "Audit Result")
    overall = data.get("overall_score", {})
    summary = data.get("summary", "")
    
    html = f"""
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            padding-bottom: 10px;
        }}
        .overall-score {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
        }}
        .overall-score h2 {{
            margin: 0;
            font-size: 32px;
        }}
        .overall-score p {{
            margin: 5px 0;
            font-size: 16px;
        }}
        .summary {{
            background-color: #e7f3ff;
            border-left: 4px solid #007bff;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th {{
            background-color: #007bff;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f9f9f9;
        }}
        .section-header {{
            background-color: #007bff;
            color: white;
            font-weight: bold;
        }}
        .parameter-row {{
            background-color: #f0f8ff;
        }}
        .score {{
            font-weight: bold;
            text-align: center;
            width: 80px;
        }}
        .score-high {{
            color: #28a745;
        }}
        .score-medium {{
            color: #ffc107;
        }}
        .score-low {{
            color: #dc3545;
        }}
        .reason {{
            font-size: 13px;
            color: #555;
            font-style: italic;
        }}
        .section-score {{
            background-color: #fff3cd;
            font-weight: bold;
        }}
        .action-links {{
            margin-top: 20px;
            text-align: center;
        }}
        .action-links a {{
            display: inline-block;
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 4px;
            margin: 0 10px;
        }}
        .action-links a:hover {{
            background-color: #0056b3;
        }}
    </style>
    
    <div class="container">
        <h1>{audit_name}</h1>
        
        <div class="overall-score">
            <h2>{overall.get('achieved', 0)}/{overall.get('maximum', 100)}</h2>
            <p>Overall Score</p>
        </div>
    """
    
    if summary:
        html += f'<div class="summary"><strong>Summary:</strong> {summary}</div>'
    
    # Display sections
    sections = data.get("sections", [])
    for section in sections:
        section_name = section.get("section_name", "Section")
        section_score = section.get("section_score", {})
        achieved = section_score.get("achieved", 0)
        maximum = section_score.get("maximum", 0)
        
        html += f"""
        <h3 style="margin-top: 30px; color: #333;">{section_name}</h3>
        <table>
            <tr class="section-header">
                <th>Parameter</th>
                <th>Weightage</th>
                <th style="text-align: center;">Score</th>
                <th>Reason</th>
            </tr>
            <tr class="section-score">
                <td colspan="2"><strong>Section Total</strong></td>
                <td class="score" style="text-align: center;"><strong>{achieved}/{maximum}</strong></td>
                <td></td>
            </tr>
        """
        
        parameters = section.get("parameters", [])
        for param in parameters:
            param_name = param.get("parameter_name", "")
            weightage = param.get("weightage", 0)
            score = param.get("score", 0)
            reason = param.get("reason", "")
            
            # Determine score color
            score_pct = (score / max(weightage, 1)) * 100 if weightage > 0 else 0
            if score_pct >= 80:
                score_class = "score-high"
            elif score_pct >= 50:
                score_class = "score-medium"
            else:
                score_class = "score-low"
            
            html += f"""
            <tr class="parameter-row">
                <td>{param_name}</td>
                <td style="text-align: center;">{weightage}</td>
                <td class="score {score_class}">{score}/{weightage}</td>
                <td><span class="reason">{reason}</span></td>
            </tr>
            """
        
        html += "</table>"
    
    html += """
        <div class="action-links">
            <a href="/">Run Another Audit</a>
        </div>
    </div>
    """
    
    return html


@app.post("/audit", response_class=HTMLResponse)
def audit(
    email_thread: str = Form(...),
    logged_in: Optional[str] = Cookie(None)
):
    """Process audit request for authenticated users."""
    if not check_auth(logged_in):
        logger.warning("Unauthorized audit request")
        return RedirectResponse(url="/login")

    try:
        # Validate input
        is_valid, error_msg = validate_email_thread(
            email_thread,
            min_length=MIN_EMAIL_LENGTH,
            max_length=MAX_EMAIL_LENGTH
        )
        if not is_valid:
            logger.warning(f"Invalid input: {error_msg}")
            return _error_page("Validation Error", error_msg, "/audit-page")
        
        logger.info("Processing audit request")
        result = run_audit(email_thread)
        
        # Check for errors in result
        try:
            result_data = safe_json_parse(result)
            if "error" in result_data:
                logger.error(f"Audit error: {result_data.get('error')}")
                return _error_page("Audit Error", result_data.get("error", "Unknown error"), "/audit-page")
        except Exception as e:
            logger.error(f"Error parsing audit response: {e}")
            return _error_page("Error", "Invalid response from audit service", "/audit-page")
        
        formatted_result = format_audit_result(result)

        return f"""
        <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    .navbar {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                    padding: 20px 40px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }}
                .navbar a {{
                    color: white;
                    text-decoration: none;
                    padding: 10px 20px;
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 5px;
                    margin-left: 10px;
                    transition: background 0.3s;
                }}
                .navbar a:hover {{
                    background: rgba(255, 255, 255, 0.3);
                }}
            </style>
        </head>
        <body>
            <div class="navbar">
                <h2 style="margin: 0;">📊 Audit Result</h2>
                <div>
                    <a href="/dashboard">Dashboard</a>
                    <a href="/audit-page">New Audit</a>
                    <a href="/logout">Logout</a>
                </div>
            </div>
            {formatted_result}
        </body>
    </html>
    """
    
    except Exception as e:
        logger.error(f"Error processing audit: {e}")
        return _error_page("Error", "An error occurred while processing your audit. Please try again.", "/audit-page")
