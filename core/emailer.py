import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_ADDRESS = "wtest5176@gmail.com"
EMAIL_PASSWORD = "eloh lpfb ouij mrvk"

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Email failed: {e}")

def generate_personalized_email(name, message):
    body = f"""
Hi {name.split()[0]},

Thanks for reaching out to GSBG Technologies. 

We’ve received your inquiry:

"{message}"

One of our Salesforce experts will get back to you shortly.  

📞 Contact us anytime: +91-9372904186
Best regards,  
GSBG Technologies Team  
www.gsbgtech.com
"""
    return body