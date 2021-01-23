from src.config import Configuration
from src.spotify_client import SpotifyClient
from src.notify import Twilio, Slack


def main():
    configuration = Configuration()
    client = SpotifyClient(configuration)

    artists_to_search = ["bab bunny", "anuel aa", "burna boy", "drake", "j balvin"]
    genres = ["afrobeat", "latin", "latino", "r-n-b", "reggeaton"]

    song_recommendations = client.top_recommended_songs(genres, artists_to_search)

    messages = [f"{s.name}: {s.uri}" for s in song_recommendations]

    Slack("tu-musica", configuration).notify("\n".join(messages))
