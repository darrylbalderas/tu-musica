from typing import List
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.common import Song, AudioFeatures
from src.config import Configuration
import json


class SpotifyClient:
    def __init__(self, config: Configuration):
        self.client = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        self.config = config

    def get_artists_uris(self, artists_to_search):
        searched_artists = {}
        artists = []
        for artist_to_search in artists_to_search:
            results = self.client.search(q=artist_to_search, limit=1)
            tracks = results['tracks']['items']
            if len(tracks) == 0:
                continue
            for track in tracks:
                for artist in track.get("artists"):
                    is_artist = artist_to_search.lower() in artist["name"].lower()
                    has_searched = artist["name"].lower() in searched_artists
                    if is_artist and not has_searched:
                        artists.append(artist["uri"])
        return artists

    def top_recommend_songs(self, genres: List[str], artists_to_search: List[str]):
        # TODO: Use Multiprocessing to pull uris
        artist_uris = self.get_artists_uris(artists_to_search)

        # TODO: Use Multiprocessing to gather recommendations
        recommendations = []
        for r in self.client.recommendations(seed_genres=genres)["tracks"]:
            recommendations.append(r)

        for r in self.client.recommendations(seed_artists=artist_uris)["tracks"]:
            recommendations.append(r)

        visited_tracks = set()
        songs = []

        for track in recommendations:
            popularity, url = track["popularity"], track['external_urls']['spotify']
            track_uri, track_name = track["uri"], track["name"]
            if track_name in visited_tracks:
                continue
            if not self.pass_audio_criteria(track_uri, track_name):
                continue
            songs.append(Song(track_name, track_uri, url, popularity))
        return self.top_songs(songs)

    def pass_audio_criteria(self, track_uri: str, track_name: str):
        audio_features = self.client.audio_features([track_uri])[0]
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

        for i, t in enumerate(sorted(tracks, key=lambda x: x.popularity, reverse=True)):
            if i >= self.config.num_top_songs:
                break
            results.append(f"{t.name}: {t.external_url}\n\n")

        return results
