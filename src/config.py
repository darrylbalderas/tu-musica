import os


class Configuration:
    def __init__(self) -> None:
        self.num_top_songs = int(os.environ.get("NUM_TOP_SONGS"))
        self.number_to_send = os.environ.get("TWILIO_NUMBER_TO_SEND")
        self.account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.number_from = os.environ.get("TWILIO_NUMBER_FROM")
