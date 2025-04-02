from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

def send_message(notification, phone_number):
    account_sid =  os.environ.get("TWILIO_SID")
    auth_token =  os.environ.get("TWILIO_TOKEN")
    client = Client(account_sid, auth_token)
    message = client.messages.create(from_ = '+15612570539',
    body=notification,
    to=str(phone_number)
    )
    print(message.sid)
    return
