from apscheduler.schedulers.background import BackgroundScheduler
from core.db import get_all_leads, update_lead_contact
from core.emailer import send_email
from datetime import datetime, timedelta

scheduler = BackgroundScheduler()

def lead_nurture_job():
    leads = get_all_leads()
    for lead in leads:
        id, name, email, msg, score, classification, last_contacted, created_at = lead
        if not last_contacted:
            continue
        last = datetime.fromisoformat(last_contacted)
        if datetime.utcnow() - last > timedelta(days=3):  # every 3 days follow-up
            subject = f"Checking in — {name}, still interested?"
            body = f"Hi {name},\n\nJust following up to see if you need help with your earlier inquiry ({classification}).\n\nBest,\nGSBG Technologies"
            send_email(email, subject, body)
            update_lead_contact(email)

def start_scheduler():
    scheduler.add_job(lead_nurture_job, 'interval', hours=12)
    scheduler.start()
