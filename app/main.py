from fastapi import FastAPI, Query
from app.services.weather_service import WeatherService
from app.repositories.s3_repository import S3Repository
from app.repositories.dynamodb_repository import DynamoDBRepository

s3_repo = S3Repository()
dynamodb_repo = DynamoDBRepository()
weather_service = WeatherService(s3_repo, dynamodb_repo)

async def lifespan(app: FastAPI):
    await s3_repo.create_bucket_if_not_exists()
    await dynamodb_repo.create_table_if_not_exists()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/weather")
async def get_weather(city: str = Query(..., min_length=1)):
    return await weather_service.get_weather(city)

