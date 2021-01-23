from twilio.rest import Client
from src.config import Configuration
from abc import ABC, abstractmethod
import requests
import json


class Notifier(ABC):
    def __init__(self, config: Configuration) -> None:
        self.config = config

    @abstractmethod
    def notify(self, message):
        pass


class Twilio(Notifier):
    def __init__(self, config: Configuration) -> None:
        if not (config.account_sid and config.auth_token):
            raise ValueError("Empty account sid or auth token")

        if not config.number_from:
            raise ValueError("Invalid Twilio phone number")

        self.client = Client(config.account_sid, config.auth_token)
        super().__init__(config)

    def notify(self, message: str):
        if not self.config.number_to_send:
            raise ValueError("Invalid phone number you are trying to send message")
        response = self.client.messages.create(
            body=message,
            from_=self.config.number_from,
            to=self.config.number_to_send,
        )
        return response


class Slack(Notifier):
    def __init__(self, app_name: str, config: Configuration) -> None:
        self.name = app_name
        super().__init__(config)

    def notify(self, message):
        data = {"text": message}
        try:
            resp = requests.post(self.config.slack_webhook,
                                 data=json.dumps(data),
                                 headers={'Content-Type': 'application/json'})
            resp.raise_for_status()
        except Exception as ex:
            print('Slack post failed: ', ex)
        else:
            return resp
