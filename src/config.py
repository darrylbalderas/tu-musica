from src.settings import NUM_TOP_SONGS, TWILIO_ACCOUNT_SID, TWILIO_NUMBER_TO_SEND
from src.settings import TWILIO_AUTH_TOKEN, TWILIO_NUMBER_FROM, SLACK_WEBHOOK


class Configuration:
    def __init__(self) -> None:
        self.num_top_songs = NUM_TOP_SONGS
        self.number_to_send = TWILIO_NUMBER_TO_SEND
        self.account_sid = TWILIO_ACCOUNT_SID
        self.auth_token = TWILIO_AUTH_TOKEN
        self.number_from = TWILIO_NUMBER_FROM
        self.slack_webhook = SLACK_WEBHOOK
