from twilio.rest import Client
def send_message(notification, phone_number):
    account_sid = 'AC79844424f42d46579da563a462d8d3f2'
    auth_token = '6fb96c876e429a27a38aecae836449d2'
    client = Client(account_sid, auth_token)
    message = client.messages.create(from_ = '+16282578173',
    body=notification,
    to=str(phone_number)
    )
    print(message.sid)
    return
