from twilio.rest import Client
account_sid = "ACa28af891c27eceb77f6c9305511d42eb"
auth_token = "43784ce5d4ee616ecd5684545d4b547f"

client = Client(account_sid,auth_token)

def send_sms(smz):
    client.messages.create(
            to="+919490932710",
            from_="+14439633415",
            body=smz
        )








