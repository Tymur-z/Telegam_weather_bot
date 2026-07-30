from datetime import datetime, timedelta, timezone

WEATHER_EMOJI = {
    "01d": "☀️", "01n": "🌙",
    "02d": "🌤️", "02n": "☁️",
    "03d": "☁️", "03n": "☁️",
    "04d": "☁️", "04n": "☁️",
    "09d": "🌧️", "09n": "🌧️",
    "10d": "🌦️", "10n": "🌧️",
    "11d": "⛈️", "11n": "⛈️",
    "13d": "❄️", "13n": "❄️",
    "50d": "🌫️", "50n": "🌫️",
}


def _local_time(unix_ts: int, tz_offset_seconds: int) -> datetime:
    """Convert a UTC unix timestamp to the queried city's local time,
    using the timezone offset OpenWeatherMap returns for that city."""
    return datetime.fromtimestamp(unix_ts, tz=timezone.utc) + timedelta(seconds=tz_offset_seconds)


def get_units_symbols(units: str) -> tuple[str, str]:
    if units == "imperial":
        return "°F", "mph"
    return "°C", "m/s"


def format_current_weather(data: dict, units: str = "metric") -> str:
    temp_symbol, wind_symbol = get_units_symbols(units)
    city = data.get("name", "-")
    country = data.get("sys", {}).get("country", "")
    tz_offset = data.get("timezone", 0)
    temp = round(data["main"]["temp"])
    feels_like = round(data["main"]["feels_like"])
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    description = data["weather"][0]["description"].capitalize()
    icon = data["weather"][0]["icon"]
    emoji = WEATHER_EMOJI.get(icon, "🌡️")

    sunrise = _local_time(data["sys"]["sunrise"], tz_offset).strftime("%H:%M")
    sunset = _local_time(data["sys"]["sunset"], tz_offset).strftime("%H:%M")

    return (
        f"{emoji} <b>Weather in {city}, {country}</b>\n\n"
        f"🌡️ Temperature: <b>{temp}{temp_symbol}</b> (feels like {feels_like}{temp_symbol})\n"
        f"📝 {description}\n"
        f"💧 Humidity: {humidity}%\n"
        f"🔵 Pressure: {pressure} hPa\n"
        f"💨 Wind: {wind_speed} {wind_symbol}\n"
        f"🌅 Sunrise: {sunrise}\n"
        f"🌇 Sunset: {sunset}\n"
    )


def format_daily_forecast(data: dict, units: str = "metric") -> str:
    """Group the 3-hour forecast into daily entries (closest to noon), for 5 days."""
    temp_symbol, _ = get_units_symbols(units)
    city_info = data.get("city", {})
    city = city_info.get("name", "-")
    tz_offset = city_info.get("timezone", 0)
    entries = data.get("list", [])

    days: dict[str, dict] = {}
    for entry in entries:
        dt = _local_time(entry["dt"], tz_offset)
        date_key = dt.strftime("%a %d %b")
        hour = dt.hour
        if date_key not in days or abs(hour - 13) < abs(days[date_key]["hour"] - 13):
            days[date_key] = {
                "hour": hour,
                "temp": round(entry["main"]["temp"]),
                "description": entry["weather"][0]["description"].capitalize(),
                "icon": entry["weather"][0]["icon"],
            }

    lines = [f"🗓️ <b>5-day forecast: {city}</b>\n"]
    for date_key, info in list(days.items())[:5]:
        emoji = WEATHER_EMOJI.get(info["icon"], "🌡️")
        lines.append(f"{emoji} <b>{date_key}</b> — {info['temp']}{temp_symbol}, {info['description']}")

    return "\n".join(lines)
