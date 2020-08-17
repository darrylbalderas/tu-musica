from dataclasses import dataclass
import os
from twilio.rest import Client
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    def __init__(self, client):
        self.client = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    def get_artists_uris(self, artists_to_search):
        artists = set()
        for a in artists_to_search:
            results = self.client.search(q=a, limit=1)
            requests_items = results['tracks']['items']
            if len(requests_items) == 0:
                continue
            for r in requests_items:
                for artist in r.get("artists"):
                    artist_name, artist_uri = artist["name"], artist["uri"]
                    if a.lower() in artist_name.lower():
                        artists.add(artist_uri)
        return artists


class TwilioClient:
    def __init__(self):
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        if not (account_sid and auth_token):
            raise ValueError("Empty account sid or auth token")
        self.from_number = os.getenv("TWILIO_FROM_NUMBER")

        if not self.from_number:
            raise ValueError("Invalid twilio phone number")

        self.client = Client(account_sid, auth_token)

    def send_messages(self, messages, to_number):
        if not to_number:
            raise ValueError("Invalid phone number you are trying to send message")
        response = self.client.messages.create(body=" ".join(messages),
                                               from_=self.from_number,
                                               to=to_number)
        return response


@dataclass
class AudioFeatures:
    name: str
    danceability: float
    energy: float
    key: float
    loudness: float
    mode: float
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float


@dataclass(frozen=True, eq=True)
class Song:
    name: str
    uri: str


def parse_audio_features(name, track):
    return AudioFeatures(name, track["danceability"], track["energy"], track["key"],
                         track["loudness"], track["mode"], track["speechiness"],
                         track["acousticness"], track["instrumentalness"],
                         track["liveness"], track["valence"], track["tempo"])


def validate_audio_features(sp, track_id):
    track_name = sp.track(track_id)["name"]
    audio_features = sp.audio_features([track_id])[0]
    track_features = parse_audio_features(track_name, audio_features)
    is_twerkable = track_features.tempo > 105 and track_features.danceability > 0.60
    is_clubworthy = track_features.loudness <= -5.0 and track_features.energy >= 0.5
    return is_twerkable and is_clubworthy


def personal_recommendations(sp, genres, artist_uris):
    recommendations = []
    recommendations.extend(sp.recommendations(seed_genres=genres)["tracks"])
    recommendations.extend(sp.recommendations(seed_artists=artist_uris)["tracks"])
    tracks = set()
    for track in recommendations:
        if not validate_audio_features(sp, track["uri"]):
            continue
        tracks.add(Song(track["name"], track["uri"]))
    return tracks


def main():
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    client = SpotifyClient(sp)

    artists_to_search = ["bab bunny", "anuel aa", "burna boy", "drake", "j balvin"]
    genres = ["afrobeat", "latin", "latino", "r-n-b", "reggeaton"]

    tracks = personal_recommendations(sp, genres,
                                      client.get_artists_uris(artists_to_search))
    top_numsongs = os.getenv("NUM_TOPSONGS", 4)

    messages = []
    for index, song in enumerate(tracks):
        if index > top_numsongs:
            break
        uri = song.uri.split(":")[-1]
        messages.append(f"{song.name}: {f'https://open.spotify.com/track/{uri}'}\n\n")

    tc = TwilioClient()
    to_number = os.getenv("TWILIO_TO_NUMBER")
    tc.send_messages(messages, to_number)


if __name__ == "__main__":
    main()
