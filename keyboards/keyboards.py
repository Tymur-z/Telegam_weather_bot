from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="🌤️ Current weather")
    builder.button(text="📅 5-day forecast")
    builder.button(text="📍 Send location", request_location=True)
    builder.button(text="⭐ Favorites")
    builder.button(text="⚙️ Settings")
    builder.button(text="ℹ️ Help")
    builder.adjust(2, 1, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def cancel_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="❌ Cancel")
    return builder.as_markup(resize_keyboard=True)


def weather_result_keyboard(city: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⭐ Add to favorites", callback_data=f"fav_add:{city}")
    builder.button(text="📅 5-day forecast", callback_data=f"forecast:{city}")
    builder.adjust(1)
    return builder.as_markup()


def favorites_keyboard(cities: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for city in cities:
        builder.button(text=f"🌍 {city}", callback_data=f"fav_weather:{city}")
        builder.button(text="🗑️", callback_data=f"fav_remove:{city}")
    builder.button(text="➕ Add a city", callback_data="fav_add_new")
    builder.adjust(2)
    return builder.as_markup()


def settings_keyboard(current_units: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    metric_mark = "✅ " if current_units == "metric" else ""
    imperial_mark = "✅ " if current_units == "imperial" else ""
    builder.button(text=f"{metric_mark}°C, m/s", callback_data="units_metric")
    builder.button(text=f"{imperial_mark}°F, mph", callback_data="units_imperial")
    builder.adjust(1)
    return builder.as_markup()
