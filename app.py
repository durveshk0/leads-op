from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from core.db import init_db, insert_lead, get_all_leads
from core.model import classify_message
from core.emailer import send_email
from core.scheduler import start_scheduler
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize
init_db()
start_scheduler()

# Admin access list
ADMIN_LIST = ["admin@gsbgtech.in", "superuser@gsbgtech.in"]

# ==========================
# 🔹 PUBLIC ROUTES
# ==========================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Public enquiry form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
async def new_lead(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    """Handle enquiry form submission"""
    score, label = classify_message(message)
    insert_lead(name, email, message, score, label)

    # Personalized thank-you mail
    body = f"""
    Hi {name},

    Thanks for contacting GSBG Technologies!
    We appreciate your message: "{message}".

    Our team will reach out shortly. 
    For quick contact, call us at +91-9XXXXXXX or reply to this email.

    Best regards,  
    Team GSBG
    """
    send_email(email, "Thanks for reaching out!", body)
    return RedirectResponse("/", status_code=303)

# ==========================
# 🔹 ADMIN ROUTES
# ==========================

@app.get("/admin-login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin-login")
async def admin_login(email: str = Form(...)):
    if email in ADMIN_LIST:
        resp = RedirectResponse("/dashboard", status_code=303)
        resp.set_cookie(key="user_email", value=email, max_age=7*24*3600)
        return resp
    return HTMLResponse("❌ Not authorized", status_code=403)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user_email = request.cookies.get("user_email")
    if not user_email or user_email not in ADMIN_LIST:
        return RedirectResponse("/admin-login")
    
    leads = get_all_leads()

    # Prioritize leads based on their classification
    prioritized_leads = sorted(leads, key=lambda l: (l[5] == "Hot", l[5] == "Warm", l[5] == "Cold"), reverse=True)

    return templates.TemplateResponse("dashboard.html", {"request": request, "leads": prioritized_leads})

@app.get("/logout")
async def logout():
    resp = RedirectResponse("/admin-login")
    resp.delete_cookie("user_email")
    return resp

# ==========================
# 🔹 API (Optional)
# ==========================

@app.get("/api/leads")
async def api_leads():
    leads = get_all_leads()
    return JSONResponse([
        {"id": l[0], "name": l[1], "email": l[2], "message": l[3],
         "score": l[4], "classification": l[5], "created_at": l[7]}
        for l in leads
    ])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
