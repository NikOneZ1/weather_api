from app.repositories.s3_repository import S3Repository
from app.repositories.dynamodb_repository import DynamoDBRepository
from app.weather import get_weather_data
import datetime

class WeatherService:
    def __init__(self, s3_repo: S3Repository, dynamodb_repo: DynamoDBRepository):
        self.s3_repo = s3_repo
        self.dynamodb_repo = dynamodb_repo

    async def get_weather(self, city: str):
        cached_data = await self.s3_repo.check_cache(city)
        if cached_data:
            return cached_data

        weather_data = await get_weather_data(city)

        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"{city}_{timestamp}.json"
        await self.s3_repo.upload_to_s3(weather_data, filename)
        await self.dynamodb_repo.log_to_dynamodb(city, timestamp, filename)

        return weather_data
