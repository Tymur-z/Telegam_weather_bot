from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.db import get_units
from keyboards.keyboards import (
    cancel_keyboard,
    main_menu_keyboard,
    weather_result_keyboard,
)
from services.weather_api import (
    CityNotFoundError,
    WeatherAPIError,
    get_current_weather,
    get_forecast,
    get_weather_by_coords,
)
from states.states import WeatherStates
from utils.formatting import format_current_weather, format_daily_forecast

router = Router()


@router.message(F.text == "🌤️ Current weather")
async def ask_city_current(message: Message, state: FSMContext):
    await state.set_state(WeatherStates.waiting_for_city)
    await message.answer("Type a city name 🏙️", reply_markup=cancel_keyboard())


@router.message(F.text == "📅 5-day forecast")
async def ask_city_forecast(message: Message, state: FSMContext):
    await state.set_state(WeatherStates.waiting_for_forecast_city)
    await message.answer("Type a city name for the forecast 🏙️", reply_markup=cancel_keyboard())


@router.message(F.text == "❌ Cancel")
async def cancel_action(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Cancelled.", reply_markup=main_menu_keyboard())


@router.message(WeatherStates.waiting_for_city)
async def process_city_current(message: Message, state: FSMContext):
    await state.clear()
    await send_current_weather(message, message.text.strip())


@router.message(WeatherStates.waiting_for_forecast_city)
async def process_city_forecast(message: Message, state: FSMContext):
    await state.clear()
    await send_forecast(message, message.text.strip())


@router.message(F.location)
async def process_location(message: Message):
    units = await get_units(message.from_user.id)
    try:
        data = await get_weather_by_coords(
            message.location.latitude, message.location.longitude, units
        )
        text = format_current_weather(data, units)
        await message.answer(text, reply_markup=weather_result_keyboard(data["name"]))
    except WeatherAPIError:
        await message.answer("⚠️ Couldn't fetch weather for your location. Please try again later.")


@router.callback_query(F.data.startswith("forecast:"))
async def callback_forecast(callback: CallbackQuery):
    city = callback.data.split(":", 1)[1]
    await callback.answer()
    await send_forecast(callback.message, city)


async def send_current_weather(message: Message, city: str):
    units = await get_units(message.from_user.id)
    try:
        data = await get_current_weather(city, units)
        text = format_current_weather(data, units)
        await message.answer(text, reply_markup=weather_result_keyboard(data["name"]))
    except CityNotFoundError:
        await message.answer(
            f"😕 City '{city}' not found. Check the spelling and try again.",
            reply_markup=main_menu_keyboard(),
        )
    except WeatherAPIError:
        await message.answer(
            "⚠️ Something went wrong while fetching the weather. Please try again later.",
            reply_markup=main_menu_keyboard(),
        )


async def send_forecast(message: Message, city: str):
    units = await get_units(message.from_user.id)
    try:
        data = await get_forecast(city, units)
        text = format_daily_forecast(data, units)
        await message.answer(text, reply_markup=main_menu_keyboard())
    except CityNotFoundError:
        await message.answer(
            f"😕 City '{city}' not found. Check the spelling and try again.",
            reply_markup=main_menu_keyboard(),
        )
    except WeatherAPIError:
        await message.answer(
            "⚠️ Something went wrong while fetching the forecast. Please try again later.",
            reply_markup=main_menu_keyboard(),
        )


# Fallback: if the user just types plain text (a city name) outside of any FSM flow,
# the bot tries to look it up directly. This handler must be registered last.
@router.message(F.text)
async def fallback_city_text(message: Message):
    text = message.text.strip()
    if text.startswith("/") or len(text) < 2:
        return
    await send_current_weather(message, text)
