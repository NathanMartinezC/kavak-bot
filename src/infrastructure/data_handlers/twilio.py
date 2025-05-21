from twilio.rest import Client
from src.infrastructure.config import settings

class TwilioClient:
    def __init__(self):
        self.client = Client(
            settings.twilio_account_sid,
            settings.twilio_auth_token,
        )

    def send_message(self, to: str, body: str):
        message = self.client.messages.create(
            body=body,
            from_=settings.twilio_from_whatsapp_number,
            to=to
        )
        return message.sid