from typing import List
from itertools import chain, islice
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.common import Song, AudioFeatures, Configuration


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

    def top_recommended_songs(self, genres: List[str], artists_to_search: List[str]):
        artist_uris = self.get_artists_uris(artists_to_search)
        visited_song_uris = set()
        songs = []

        for recommend_song in self.generate_song_recommendations(genres, artist_uris):
            song = Song(
                recommend_song["name"],
                recommend_song["uri"],
                recommend_song["external_urls"]["spotify"],
                recommend_song["popularity"],
            )

            if song.uri in visited_song_uris:
                continue

            if not self.is_valid_audio_features(song.uri, song.name):
                continue

            songs.append(song)
        return self.top_songs(songs)

    def generate_song_recommendations(self, genres, artist_uris):
        return chain(
            self.client.recommendations(seed_genres=genres)["tracks"],
            self.client.recommendations(seed_artists=artist_uris)["tracks"],
        )

    def is_valid_audio_features(self, song_uri: str, song_name: str):
        try:
            audio_features = self.client.audio_features([song_uri])[0]
        except Exception as e:
            print(e)
            return False
        track_features = self.parse_audio_features(song_name, audio_features)
        return track_features.is_twerkable() and track_features.is_clubworthy()

    @staticmethod
    def parse_audio_features(song_name: str, audio_features: dict):
        return AudioFeatures(
            song_name,
            audio_features["danceability"],
            audio_features["energy"],
            audio_features["key"],
            audio_features["loudness"],
            audio_features["mode"],
            audio_features["speechiness"],
            audio_features["acousticness"],
            audio_features["instrumentalness"],
            audio_features["liveness"],
            audio_features["valence"],
            audio_features["tempo"],
        )

    def top_songs(self, songs):
        return islice(
            sorted(songs, key=lambda x: x.popularity, reverse=True),
            self.config.num_top_songs,
        )
