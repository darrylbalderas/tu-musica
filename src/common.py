from dataclasses import dataclass


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
    external_url: str
    popularity: int
