"""
Unit tests for the pure formatting helpers in utils/formatting.py.
No network access or API keys are needed to run these.

Run with:  python -m pytest
"""

import time

from utils.formatting import (
    format_current_weather,
    format_daily_forecast,
    get_units_symbols,
)


def test_units_symbols_metric():
    temp, wind = get_units_symbols("metric")
    assert temp == "°C"
    assert wind == "m/s"


def test_units_symbols_imperial():
    temp, wind = get_units_symbols("imperial")
    assert temp == "°F"
    assert wind == "mph"


def test_format_current_weather_contains_key_fields():
    sample = {
        "name": "Portsmouth",
        "sys": {
            "country": "GB",
            "sunrise": int(time.time()) - 3600,
            "sunset": int(time.time()) + 3600 * 8,
        },
        "timezone": 0,
        "main": {"temp": 18.4, "feels_like": 17.9, "humidity": 72, "pressure": 1012},
        "wind": {"speed": 4.1},
        "weather": [{"description": "scattered clouds", "icon": "02d"}],
    }

    result = format_current_weather(sample, "metric")

    assert "Portsmouth" in result
    assert "GB" in result
    assert "18°C" in result
    assert "72%" in result
    assert "Scattered clouds" in result


def test_format_daily_forecast_groups_by_day():
    now = int(time.time())
    sample = {
        "city": {"name": "London", "timezone": 0},
        "list": [
            {
                "dt": now + i * 3 * 3600,
                "main": {"temp": 15 + i},
                "weather": [{"description": "clear sky", "icon": "01d"}],
            }
            for i in range(16)
        ],
    }

    result = format_daily_forecast(sample, "metric")

    assert "London" in result
    assert "5-day forecast" in result
