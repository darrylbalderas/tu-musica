from platform import version
from src.spotify_client import SpotifyClient
from src.notify import Slack
from src.common import Configuration
from src import settings
from src.store import PreferencesStore


def grab_preferences(configuration: Configuration) -> dict:
    store = PreferencesStore(configuration.aws_region)

    if configuration.db_reset:
        store.remove_table(configuration.db_table)

    if not store.table_exist(configuration.db_table):
        key_schema = [{"AttributeName": "stage", "KeyType": "HASH"}]
        attribute_definition = [{"AttributeName": "stage", "AttributeType": "S"}]
        throughput = {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
        store.create_table(configuration.db_table, key_schema, attribute_definition,
                           throughput)

    return store.grab_preferences(environment="test",
                                  version="0.0.1",
                                  table_name=configuration.db_table,
                                  load_from_local=configuration.load_from_local)


def main():
    configuration = Configuration(
        num_top_songs=settings.NUM_TOP_SONGS,
        number_to_send=settings.TWILIO_NUMBER_TO_SEND,
        account_sid=settings.TWILIO_ACCOUNT_SID,
        auth_token=settings.TWILIO_AUTH_TOKEN,
        number_from=settings.TWILIO_NUMBER_FROM,
        slack_webhook=settings.SLACK_WEBHOOK,
        aws_region=settings.AWS_REGION,
        db_reset=settings.DB_RESET,
        db_table=settings.DB_TABLE,
        load_from_local=settings.LOAD_FROM_LOCAL,
    )

    client = SpotifyClient(configuration)
    preferences = grab_preferences(configuration=configuration)

    song_recommendations = client.top_recommended_songs(preferences["music"]["genres"],
                                                        preferences["music"]["artists"])

    messages = [f"{s.name}: {s.uri}" for s in song_recommendations]
    Slack(app_name="tu-musica", configuration=configuration).notify("\n".join(messages))
