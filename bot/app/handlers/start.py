from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from app.db.func import get_or_create_user, set_export_enabled
from app.page.start import send_main_menu


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = int(message.from_user.id)
    user_name = message.from_user.full_name
    user = await get_or_create_user(user_id, user_name)
    await send_main_menu(message, user)


@router.message(F.text.in_(["❌ Отключить выгрузку в GS", "✅ Включить выгрузку в GS"]))
async def admin_export_to_gs(message: Message):
    user_id = int(message.from_user.id)
    user = await get_or_create_user(user_id)
    if user.is_admin:
        export_allowed = message.text == "✅ Включить выгрузку в GS"
        await set_export_enabled(export_allowed)
        await send_main_menu(message, user)


@router.message(F.text == "⬅️ Назад", StateFilter("*"))
async def handle_back(message: Message, state: FSMContext):
    await state.clear()
    user_id = int(message.from_user.id)
    user = await get_or_create_user(user_id)
    await send_main_menu(message, user)
