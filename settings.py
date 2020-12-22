# settings.py
from dotenv import load_dotenv
import os

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TO_NUMBER = os.getenv("TWILIO_TO_NUMBER")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
NUM_TOPSONGS = os.getenv("NUM_TOPSONGS")