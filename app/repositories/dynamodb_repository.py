from app.factories.boto3_client_factory import Boto3ClientFactory
from app.config import Config

class DynamoDBRepository:
    def __init__(self):
        self.table = Config.AWS_DYNAMODB_TABLE
        self.client_factory = Boto3ClientFactory()

    async def create_table_if_not_exists(self):
        async with await self.client_factory.get_client('dynamodb') as dynamodb:
            try:
                await dynamodb.describe_table(TableName=self.table)
            except dynamodb.exceptions.ResourceNotFoundException:
                await dynamodb.create_table(
                    TableName=self.table,
                    KeySchema=[
                        {'AttributeName': 'City', 'KeyType': 'HASH'},
                        {'AttributeName': 'Timestamp', 'KeyType': 'RANGE'}
                    ],
                    AttributeDefinitions=[
                        {'AttributeName': 'City', 'AttributeType': 'S'},
                        {'AttributeName': 'Timestamp', 'AttributeType': 'S'}
                    ],
                    ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
                )

    async def log_to_dynamodb(self, city: str, timestamp: str, filename: str):
        async with await self.client_factory.get_client('dynamodb') as dynamodb:
            await dynamodb.put_item(
                TableName=self.table,
                Item={
                    'City': {'S': city},
                    'Timestamp': {'S': timestamp},
                    'Filename': {'S': filename}
                }
            )

