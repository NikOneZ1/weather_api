import os

class Config:
    API_KEY = os.getenv('API_KEY')
    BASE_URL = os.getenv('BASE_URL')
    AWS_REGION = os.getenv('AWS_REGION')
    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')
    AWS_DYNAMODB_TABLE = os.getenv('AWS_DYNAMODB_TABLE')
    AWS_HOST = os.getenv('AWS_HOST')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    CACHE_EXPIRATION_MINUTES = int(os.getenv('CACHE_EXPIRATION_MINUTES', 5))
