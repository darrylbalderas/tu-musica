import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.common import Song, AudioFeatures
from src.config import Configuration


class SpotifyClient:
    def __init__(self, config: Configuration):
        self.client = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        self.config = config

    def get_artists_uris(self, artists_to_search):
        artists = set()
        for artist_to_search in artists_to_search:
            results = self.client.search(q=artist_to_search, limit=1)
            tracks = results['tracks']['items']
            if len(tracks) == 0:
                continue
            for track in tracks:
                for artist in track.get("artists"):
                    if artist_to_search.lower() in artist["name"].lower():
                        artists.add(artist["uri"])
        return artists

    def personal_recommendations(self, genres, artists_to_search):
        artist_uris = self.get_artists_uris(artists_to_search)
        recommendations = [] + self.client.recommendations(
            seed_genres=genres)["tracks"] + self.client.recommendations(
                seed_artists=artist_uris)["tracks"]
        tracks = set()
        for track in recommendations:
            uri, song = track["uri"], track["name"]
            if not self.validate_audio_features(uri):
                continue
            tracks.add(Song(song, uri))
        return list(tracks)

    def validate_audio_features(self, track_id: str):
        track_name = self.client.track(track_id)["name"]
        audio_features = self.client.audio_features([track_id])[0]
        track_features = self.parse_audio_features(track_name, audio_features)
        # TODO: Create SongFilter Class
        is_twerkable = track_features.tempo > 105 and track_features.danceability > 0.60
        is_clubworthy = track_features.loudness <= -5.0 and track_features.energy >= 0.5
        return is_twerkable and is_clubworthy

    def parse_audio_features(self, name: str, track: dict):
        return AudioFeatures(name, track["danceability"], track["energy"], track["key"],
                             track["loudness"], track["mode"], track["speechiness"],
                             track["acousticness"], track["instrumentalness"],
                             track["liveness"], track["valence"], track["tempo"])

    def top_songs(self, tracks):
        results = []
        for i in range(self.config.num_top_songs):
            uri, song, = tracks[i].uri, tracks[i].name
            uri = uri.split(":")[-1]
            results.append(f"{song}: {f'https://open.spotify.com/track/{uri}'}\n\n")
        return results
