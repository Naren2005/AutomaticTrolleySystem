from twilio.rest import Client
account_sid = "ACa28af891c27eceb77f6c9305511d42eb"
auth_token = "041b6ea21afa1c743a109642161cc32d"

client = Client(account_sid,auth_token)

def send_sms(sms):
    client.messages.create(
        to="+919490932710",
        from_="+14439633415",
        body=sms
    )

