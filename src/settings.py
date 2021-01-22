# settings.py
from dotenv import load_dotenv
import os

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_NUMBER_TO_SEND = os.getenv("TWILIO_NUMBER_TO_SEND")
TWILIO_NUMBER_FROM = os.getenv("TWILIO_NUMBER_FROM")
NUM_TOP_SONGS = int(os.getenv("NUM_TOP_SONGS"))
