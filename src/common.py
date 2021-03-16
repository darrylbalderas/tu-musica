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

    def is_twerkable(self):
        return self.tempo > 105 and self.danceability > 0.60

    def is_clubworthy(self):
        return self.loudness <= -5.0 and self.energy >= 0.5


@dataclass(frozen=True, eq=True)
class Song:
    name: str
    uri: str
    external_url: str
    popularity: int


@dataclass
class Configuration:
    num_top_songs: int
    account_sid: str
    number_to_sd: str
    number_from: str
    auth_token: str
    aws_region: str
    slack_webhook: str
