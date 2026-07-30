from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from database.db import get_units, set_units
from keyboards.keyboards import settings_keyboard

router = Router()


@router.message(F.text == "⚙️ Settings")
async def show_settings(message: Message):
    units = await get_units(message.from_user.id)
    await message.answer(
        "⚙️ <b>Settings</b>\n\nChoose your preferred units:",
        reply_markup=settings_keyboard(units),
    )


@router.callback_query(F.data.in_({"units_metric", "units_imperial"}))
async def change_units(callback: CallbackQuery):
    units = "metric" if callback.data == "units_metric" else "imperial"
    await set_units(callback.from_user.id, units)
    await callback.answer("Units updated ✅")
    await callback.message.edit_text(
        "⚙️ <b>Settings</b>\n\nChoose your preferred units:",
        reply_markup=settings_keyboard(units),
    )
