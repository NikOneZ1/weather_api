from app.factories.boto3_client_factory import Boto3ClientFactory
import json
from datetime import datetime, timedelta
from app.config import Config

class S3Repository:
    def __init__(self):
        self.bucket = Config.AWS_S3_BUCKET
        self.cache_expiration_minutes = Config.CACHE_EXPIRATION_MINUTES
        self.client_factory = Boto3ClientFactory()

    async def create_bucket_if_not_exists(self):
        async with await self.client_factory.get_client('s3') as s3:
            try:
                await s3.head_bucket(Bucket=self.bucket)
            except s3.exceptions.ClientError:
                await s3.create_bucket(Bucket=self.bucket)

    async def upload_to_s3(self, data, filename):
        async with await self.client_factory.get_client('s3') as s3:
            await s3.put_object(Bucket=self.bucket, Key=filename, Body=json.dumps(data))

    async def check_cache(self, city: str):
        async with await self.client_factory.get_client('s3') as s3:
            try:
                response = await s3.list_objects_v2(Bucket=self.bucket, Prefix=city)
                if 'Contents' in response:
                    for obj in response['Contents']:
                        timestamp_str = obj['Key'].split('_')[1].replace('.json', '')
                        timestamp = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
                        if datetime.utcnow() - timestamp < timedelta(minutes=self.cache_expiration_minutes):
                            cached_obj = await s3.get_object(Bucket=self.bucket, Key=obj['Key'])
                            return json.loads(await cached_obj['Body'].read())
            except s3.exceptions.NoSuchBucket:
                return None
            return None

