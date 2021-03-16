from datetime import datetime
import yaml
from botocore.client import Config
from botocore.exceptions import ClientError
import boto3


class PreferencesStore:
    def __init__(self, region, environment="development", timeout=5, max_retries=0):
        config = Config(
            connect_timeout=timeout,
            retries={"max_attempts": max_retries},
            region_name=region,
        )
        if environment == "production":
            self.client = boto3.client("dynamodb")
            self.resource = boto3.resource("dynamodb")
        else:
            self.client = boto3.client("dynamodb",
                                       config=config,
                                       endpoint_url="http://localhost:8000")
            self.resource = boto3.resource("dynamodb",
                                           config=config,
                                           endpoint_url="http://localhost:8000")

    def table_exist(self, table_name):
        table = None
        try:
            table = self.client.describe_table(TableName=table_name)
        except ClientError as e:
            print(e)
        return table is not None

    def get_table(self, table):
        if not self.table_exist(table):
            return None
        return self.resource.Table(table)

    def grab_preferences(self,
                         environment: str,
                         version: str,
                         table_name: str,
                         load_from_local: bool = False) -> dict:

        table = self.get_table(table_name)
        key = f"{environment.upper()}-{version}"

        if load_from_local:
            table.put_item(
                Item={
                    "environment": key,
                    "music": self.load_preferences(),
                    "created_at": datetime.utcnow().isoformat(),
                })

        result = self.get_table(table_name).get_item(Key={
            "environment": key
        }).get("Item")

        if not result:
            print("Empty result")

        return result

    @staticmethod
    def load_preferences(file: str = "preferences.yml"):
        with open(file) as fin:
            return yaml.load(fin, Loader=yaml.SafeLoader)

    def create_table(self, table_name, key_schema, attribute_definition, throughput):
        table = self.resource.create_table(
            TableName=table_name,
            AttributeDefinitions=attribute_definition,
            KeySchema=key_schema,
            ProvisionedThroughput=throughput,
        )
        # Wait until the table exists.
        table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
        return table

    def remove_table(self, table_name):
        return self.client.delete_table(TableName=table_name)
