from src.config import Configuration
from src.spotify_client import SpotifyClient
from src.twilio_client import TwilioClient


def main():
    configuration = Configuration()
    client = SpotifyClient(configuration)

    artists_to_search = ["bab bunny", "anuel aa", "burna boy", "drake", "j balvin"]
    genres = ["afrobeat", "latin", "latino", "r-n-b", "reggeaton"]

    client.top_songs(client.personal_recommendations(genres, artists_to_search))

    songs = client.top_songs(client.personal_recommendations(genres, artists_to_search))

    print(songs)

    # tc = TwilioClient(configuration)

    # tc.send_messages(songs)
