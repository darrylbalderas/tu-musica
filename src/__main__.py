from src.config import Configuration
from src.spotify_client import SpotifyClient
from src.notify import Twilio, Slack


def main():
    configuration = Configuration()
    client = SpotifyClient(configuration)

    artists_to_search = ["bab bunny", "anuel aa", "burna boy", "drake", "j balvin"]
    genres = ["afrobeat", "latin", "latino", "r-n-b", "reggeaton"]

    recommend_songs = client.top_recommend_songs(genres, artists_to_search)

    messages = [f"{s.name}: {s.external_url}\n\n" for s in recommend_songs]

    Slack("tu-musica", configuration).notify("".join(messages))
