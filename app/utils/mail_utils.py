import requests
import json
from app.config import email_from, brevo_api_key

def send_mail(to_email: str, subject: str, text_content: str):
  url = "https://api.brevo.com/v3/smtp/email"
  payload = json.dumps(
      {
          "sender": {"name": "Car rental", "email": email_from},
          "to": [{"email": f"{to_email}"}],
          "subject": subject,
          "textContent": text_content,
      }
  )
  headers = {
      "accept": "application/json",
      "api-key": brevo_api_key,
      "content-type": "application/json",
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  print(response.text)
  return