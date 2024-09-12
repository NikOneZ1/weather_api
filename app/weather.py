import aiohttp

from fastapi import HTTPException

from app.config import Config


async def get_weather_data(city: str):
    url = f"{Config.BASE_URL}?q={city}&appid={Config.API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_message = await response.json()
                raise HTTPException(status_code=response.status, detail=error_message.get('message', 'Unknown error'))
