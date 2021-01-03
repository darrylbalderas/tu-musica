from twilio.rest import Client
from src.config import Configuration


class TwilioClient:
    def __init__(self, config: Configuration):
        if not (config.account_sid and config.auth_token):
            raise ValueError("Empty account sid or auth token")

        if not config.number_from:
            raise ValueError("Invalid twilio phone number")

        self.client = Client(config.account_sid, config.auth_token)
        self.config = config

    def send_messages(self, messages):
        if not self.config.number_to_send:
            raise ValueError("Invalid phone number you are trying to send message")
        response = self.client.messages.create(
            body=" ".join(messages),
            from_=self.config.number_from,
            to=self.config.number_to_send,
        )
        return response
