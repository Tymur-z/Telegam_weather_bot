from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from database.db import get_or_create_user
from keyboards.keyboards import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await get_or_create_user(message.from_user.id)
    text = (
        f"Hi, {message.from_user.first_name}! 👋\n\n"
        "I'm a weather bot 🌦️\n\n"
        "What I can do:\n"
        "🌤️ Show the current weather for any city\n"
        "📅 Show a 5-day forecast\n"
        "📍 Detect weather from your location\n"
        "⭐ Save favorite cities for quick access\n"
        "⚙️ Switch between °C and °F\n\n"
        "Pick an option from the keyboard below 👇\n"
        "Or just type a city name!"
    )
    await message.answer(text, reply_markup=main_menu_keyboard())


@router.message(Command("help"))
@router.message(F.text == "ℹ️ Help")
async def cmd_help(message: Message):
    text = (
        "<b>How to use this bot:</b>\n\n"
        "🌤️ <b>Current weather</b> — get the current weather for a city\n"
        "📅 <b>5-day forecast</b> — see the forecast for the next few days\n"
        "📍 <b>Send location</b> — get the weather for where you are\n"
        "⭐ <b>Favorites</b> — saved cities for quick access\n"
        "⚙️ <b>Settings</b> — choose units of measurement\n\n"
        "You can also just type a city name — the bot will reply straight away!"
    )
    await message.answer(text)
