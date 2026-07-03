import requests
import os
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(message: str) -> dict:
    try:
       response = requests.post(url, json={"text": message})
       if response.status_code == 200:
          return {"success": True}
       else:
          return {"success": False, "message": response.text}
    except Exception as e:
        return {"success": False, "message": str(e)}