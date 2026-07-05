from dotenv import load_dotenv
load_dotenv()
import os 
from email.mime.text import MIMEText
import smtplib

def send_email_alert(subject: str, body:str)-> dict:
    try:
        sender = os.getenv("EMAIL_SENDER")
        password = os.getenv("EMAIL_PASSWORD")
        receiver = os.getenv("EMAIL_RECEIVER")

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        return {"success": True, "message": "Email Sent"}

    except Exception as e:
        return {"success": False, "message": str(e)}


