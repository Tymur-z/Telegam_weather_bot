"""
Thin async wrapper around OpenWeatherMap's free "Current Weather Data" and
"5 Day / 3 Hour Forecast" endpoints (/data/2.5/...).

These endpoints are part of OpenWeatherMap's permanently free tier:
no credit card required, up to 60 calls/minute and 1,000,000 calls/month.
See: https://openweathermap.org/price
"""

import aiohttp

from config import OWM_API_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5"


class WeatherAPIError(Exception):
    """Generic error raised when the weather API call fails."""


class CityNotFoundError(WeatherAPIError):
    """Raised when the requested city could not be found."""


async def _get_json(session: aiohttp.ClientSession, path: str, params: dict) -> dict:
    async with session.get(f"{BASE_URL}/{path}", params=params) as resp:
        data = await resp.json()
        if resp.status == 404:
            raise CityNotFoundError(f"City '{params.get('q')}' not found")
        if resp.status != 200:
            raise WeatherAPIError(data.get("message", "Unknown API error"))
        return data


async def get_current_weather(city: str, units: str = "metric", lang: str = "en") -> dict:
    params = {"q": city, "appid": OWM_API_KEY, "units": units, "lang": lang}
    async with aiohttp.ClientSession() as session:
        return await _get_json(session, "weather", params)


async def get_weather_by_coords(
    lat: float, lon: float, units: str = "metric", lang: str = "en"
) -> dict:
    params = {"lat": lat, "lon": lon, "appid": OWM_API_KEY, "units": units, "lang": lang}
    async with aiohttp.ClientSession() as session:
        return await _get_json(session, "weather", params)


async def get_forecast(city: str, units: str = "metric", lang: str = "en") -> dict:
    params = {"q": city, "appid": OWM_API_KEY, "units": units, "lang": lang}
    async with aiohttp.ClientSession() as session:
        return await _get_json(session, "forecast", params)
