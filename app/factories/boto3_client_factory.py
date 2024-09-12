import aioboto3
from app.config import Config

class Boto3ClientFactory:
    def __init__(self):
        self.session = aioboto3.Session()
        self.aws_host = Config.AWS_HOST
        self.aws_region = Config.AWS_REGION
        self.aws_access_key_id = Config.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY

    async def get_client(self, service_name: str):
        """
        Get a client for a given AWS service (e.g., S3, DynamoDB).
        """
        return self.session.client(
            service_name,
            endpoint_url=self.aws_host,
            region_name=self.aws_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
