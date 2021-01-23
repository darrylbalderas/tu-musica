from typing import List
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.common import Song, AudioFeatures
from src.config import Configuration
from itertools import chain, islice


class SpotifyClient:
    def __init__(self, config: Configuration):
        self.client = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
        self.config = config

    def get_artists_uris(self, artists_to_search):
        searched_artists = {}
        uris = []
        for artist_to_search, tracks in self.search_artist_tracks(artists_to_search):
            for track in tracks:
                for artist in track.get("artists"):
                    is_artist = artist_to_search in artist["name"].lower()
                    has_searched = artist["name"].lower() in searched_artists
                    if is_artist and not has_searched:
                        uris.append(artist["uri"])
        return uris

    def search_artist_tracks(self, artists_to_search):
        for artist_to_search in artists_to_search:
            results = self.client.search(q=artist_to_search, limit=1)
            tracks = results["tracks"]["items"]
            if len(tracks) == 0:
                continue
            yield artist_to_search.lower(), tracks

    def top_recommend_songs(self, genres: List[str], artists_to_search: List[str]):
        # TODO: Use Multiprocessing to pull uris
        artist_uris = self.get_artists_uris(artists_to_search)

        visited_tracks = set()
        songs = []

        # TODO: Use Multiprocessing to gather recommendations
        for track in self.recommend_tracks(genres, artist_uris):
            song = Song(
                track["name"],
                track["uri"],
                track["external_urls"]["spotify"],
                track["popularity"],
            )
            if song.name in visited_tracks:
                continue

            if not self.pass_audio_criteria(song.uri, song.name):
                continue
            songs.append(song)
        return self.top_songs(songs)

    def recommend_tracks(self, genres, artist_uris):
        return chain(
            self.client.recommendations(seed_genres=genres)["tracks"],
            self.client.recommendations(seed_artists=artist_uris)["tracks"],
        )

    def pass_audio_criteria(self, track_uri: str, track_name: str):
        # TODO: Handle 503 errors for getting audio features
        try:
            audio_features = self.client.audio_features([track_uri])[0]
        except Exception as e:
            print(e)
            return False
        # TODO: Parse id, duration_ms
        track_features = self.parse_audio_features(track_name, audio_features)
        return track_features.is_twerkable() and track_features.is_clubworthy()

    def parse_audio_features(self, name: str, track: dict):
        return AudioFeatures(
            name,
            track["danceability"],
            track["energy"],
            track["key"],
            track["loudness"],
            track["mode"],
            track["speechiness"],
            track["acousticness"],
            track["instrumentalness"],
            track["liveness"],
            track["valence"],
            track["tempo"],
        )

    def top_songs(self, songs):
        return islice(
            sorted(songs, key=lambda x: x.popularity, reverse=True),
            self.config.num_top_songs,
        )
