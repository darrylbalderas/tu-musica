import os
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_NUMBER_TO_SEND = os.getenv("TWILIO_NUMBER_TO_SEND")
TWILIO_NUMBER_FROM = os.getenv("TWILIO_NUMBER_FROM")
NUM_TOP_SONGS = int(os.getenv("NUM_TOP_SONGS"))
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")
AWS_REGION = os.getenv("AWS_REGION")
DB_RESET = bool(os.getenv("DB_RESET", 0))
LOAD_FROM_LOCAL = bool(os.getenv("LOAD_FROM_LOCAL", 0))
DB_TABLE = os.getenv("DB_TABLE")
