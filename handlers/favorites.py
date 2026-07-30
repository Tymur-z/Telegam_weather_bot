from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.db import add_favorite, get_favorites, get_units, remove_favorite
from keyboards.keyboards import (
    cancel_keyboard,
    favorites_keyboard,
    main_menu_keyboard,
    weather_result_keyboard,
)
from services.weather_api import CityNotFoundError, WeatherAPIError, get_current_weather
from states.states import FavoritesStates
from utils.formatting import format_current_weather

router = Router()


@router.message(F.text == "⭐ Favorites")
async def show_favorites(message: Message):
    cities = await get_favorites(message.from_user.id)
    if not cities:
        await message.answer(
            "You don't have any favorite cities yet.\n"
            "Add one from a weather result by tapping '⭐ Add to favorites'."
        )
        return
    await message.answer("⭐ <b>Your favorite cities:</b>", reply_markup=favorites_keyboard(cities))


@router.callback_query(F.data.startswith("fav_add:"))
async def add_to_favorites(callback: CallbackQuery):
    city = callback.data.split(":", 1)[1]
    added = await add_favorite(callback.from_user.id, city)
    if added:
        await callback.answer(f"'{city}' added to favorites ⭐")
    else:
        await callback.answer("This city is already in your favorites ✅")


@router.callback_query(F.data == "fav_add_new")
async def add_new_favorite(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(FavoritesStates.waiting_for_city_to_add)
    await callback.message.answer(
        "Type the name of the city you'd like to add to favorites:",
        reply_markup=cancel_keyboard(),
    )


@router.message(FavoritesStates.waiting_for_city_to_add)
async def process_new_favorite(message: Message, state: FSMContext):
    await state.clear()
    city = message.text.strip()
    units = await get_units(message.from_user.id)
    try:
        data = await get_current_weather(city, units)  # also validates the city exists
        real_name = data["name"]
        added = await add_favorite(message.from_user.id, real_name)
        if added:
            await message.answer(f"'{real_name}' added to favorites ⭐", reply_markup=main_menu_keyboard())
        else:
            await message.answer(f"'{real_name}' is already in your favorites ✅", reply_markup=main_menu_keyboard())
    except CityNotFoundError:
        await message.answer(f"😕 City '{city}' not found.", reply_markup=main_menu_keyboard())
    except WeatherAPIError:
        await message.answer("⚠️ Something went wrong while checking that city.", reply_markup=main_menu_keyboard())


@router.callback_query(F.data.startswith("fav_remove:"))
async def remove_from_favorites(callback: CallbackQuery):
    city = callback.data.split(":", 1)[1]
    await remove_favorite(callback.from_user.id, city)
    cities = await get_favorites(callback.from_user.id)
    await callback.answer(f"'{city}' removed from favorites 🗑️")
    if cities:
        await callback.message.edit_text(
            "⭐ <b>Your favorite cities:</b>", reply_markup=favorites_keyboard(cities)
        )
    else:
        await callback.message.edit_text("You don't have any favorite cities left.")


@router.callback_query(F.data.startswith("fav_weather:"))
async def weather_for_favorite(callback: CallbackQuery):
    city = callback.data.split(":", 1)[1]
    units = await get_units(callback.from_user.id)
    await callback.answer()
    try:
        data = await get_current_weather(city, units)
        text = format_current_weather(data, units)
        await callback.message.answer(text, reply_markup=weather_result_keyboard(data["name"]))
    except (CityNotFoundError, WeatherAPIError):
        await callback.message.answer("⚠️ Couldn't fetch weather for this city.")
